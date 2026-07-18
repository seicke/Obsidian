import re
import win32com.client
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pathlib import Path
from datetime import date

DOC_ID = "L_202601778"

SOURCES = {
    "de": f"https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=OJ:{DOC_ID}",
    "en": f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:{DOC_ID}",
}

SCRIPT_DIR = Path(__file__).parent
TARGET_DIR = (SCRIPT_DIR / "../../00 Inbox").resolve()
OUTPUT_FILE = TARGET_DIR / f"{DOC_ID}.md"

PROXY = "http://proxyespel.harting.intra:80"
WINHTTP_ACCESS_TYPE_NAMED_PROXY = 2
WINHTTP_AUTOLOGON_SECURITY_LEVEL_LOW = 0


def fetch_html(url: str) -> str:
    """Fetch raw HTML from the given URL via WinHttp with proxy support."""
    http = win32com.client.Dispatch("WinHttp.WinHttpRequest.5.1")
    http.SetProxy(WINHTTP_ACCESS_TYPE_NAMED_PROXY, PROXY)
    http.SetAutoLogonPolicy(WINHTTP_AUTOLOGON_SECURITY_LEVEL_LOW)
    http.Open("GET", url, False)
    http.Send()

    if http.Status != 200:
        raise ConnectionError(f"HTTP {http.Status} for URL: {url}")

    return bytes(http.ResponseBody).decode("utf-8")


def extract_title(html: str, fallback: str) -> str:
    """Extract document title from HTML body headings or <title> tag."""
    soup = BeautifulSoup(html, "html.parser")

    if soup.body:
        for tag in ["h1", "h2"]:
            heading = soup.body.find(tag)
            if heading:
                return heading.get_text(separator=" ", strip=True)

    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text(strip=True)

    return fallback


def preprocess_html(html: str) -> str:
    """Strip EUR-Lex layout elements before markdown conversion.

    Unwraps all table-related tags so their content flows as plain blocks.
    Removes <hr> tags that produce spurious horizontal rules in markdown.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove <hr> tags — they produce stray --- lines in markdown
    for hr in soup.find_all("hr"):
        hr.decompose()

    # Unwrap table structure tags in correct bottom-up order.
    # EUR-Lex uses <table> for layout (recitals, numbered items), not data.
    for tag_name in ["td", "th", "tr", "tbody", "thead", "tfoot", "table"]:
        for tag in soup.find_all(tag_name):
            tag.unwrap()

    return str(soup)

def html_to_markdown(html: str) -> str:
    """Convert HTML to clean Markdown.

    Pre-processes HTML to remove layout tables and horizontal rules.
    Collapses excessive blank lines and merges dangling list markers with their content.
    Normalises multiple spaces after list markers to a single space.
    Removes blank lines between consecutive list items.
    Converts standalone 'Artikel N' / 'Article N' lines to #### headings.
    Merges article number heading with the following title line.
    Strips trailing whitespace from each line.
    """
    cleaned_html = preprocess_html(html)
    raw = md(cleaned_html, heading_style="ATX", strip=["script", "style", "head"])

    # Collapse 3+ consecutive newlines to one blank line
    result = re.sub(r"\n{3,}", "\n\n", raw)

    # Merge dangling list markers with their content paragraph
    result = re.sub(r"(?m)^([a-z]\)|\([0-9a-z]+\)|[0-9]+\.)\s*\n\n+", r"\1 ", result)

    # Collapse multiple spaces after list markers to a single space
    result = re.sub(r"(?m)^([a-z]\)|\([0-9a-z]+\)|[0-9]+\.)\s{2,}", r"\1 ", result)

    # Remove blank lines between consecutive list items
    result = re.sub(r"\n\n(?=(?:[a-z]\)|\([0-9a-z]+\)|[0-9]+\.) )", "\n", result)

    # Convert standalone 'Artikel N' / 'Article N' lines to #### headings
    result = re.sub(r"(?m)^(Artikel|Article)\s([0-9a-z]+)$", r"#### \1 \2", result)

    # Merge article heading with the following title line
    result = re.sub(r"(?m)^(#### (?:Artikel|Article)\s[0-9a-z]+)\n\n(.+)$", r"\1 \2", result)

    # Strip trailing whitespace per line
    result = "\n".join(line.rstrip() for line in result.split("\n"))

    return result.strip()



html_de = fetch_html(SOURCES["de"])
html_en = fetch_html(SOURCES["en"])

doc_title = extract_title(html_de, fallback=f"Verordnung {DOC_ID}")

content_de = html_to_markdown(html_de)
content_en = html_to_markdown(html_en)

frontmatter = f"""---
title: "{doc_title}"
aliases:
        - "{DOC_ID}"
source_de: "{SOURCES['de']}"
source_en: "{SOURCES['en']}"
date_fetched: {date.today().isoformat()}
languages:
        - DE
        - EN
tags:
        - EU-Recht
        - Verordnung
        - bilingual
created: {date.today().strftime("%Y-%m-%d %H:%M:%S")}
updated: {date.today().strftime("%Y-%m-%d %H:%M:%S")}
---

"""

note = (
    frontmatter
        + f"# {doc_title}\n\n"
        + "## 🇩🇪 Deutsch\n\n"
        + content_de
        + "\n\n---\n\n"
        + "## 🇬🇧 English\n\n"
        + content_en
)

OUTPUT_FILE.write_text(note, encoding="utf-8")
