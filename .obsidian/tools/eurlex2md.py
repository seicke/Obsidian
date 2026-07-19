import re
import win32com.client
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pathlib import Path
from datetime import date

DOC_ID = "L_202401781"

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
    """Extract document title from HTML body headings or <title> tag.

    Skips headings that match the .fmx.xml filename pattern.
    """
    soup = BeautifulSoup(html, "html.parser")

    if soup.body:
        for tag in ["h1", "h2", "p"]:
            for heading in soup.body.find_all(tag):
                text = heading.get_text(separator=" ", strip=True)
                if text and not re.search(r"\.fmx\.xml$", text):
                    return text

    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text(strip=True)

    return fallback

from bs4 import BeautifulSoup, ProcessingInstruction


def preprocess_html(html: str) -> str:
    """Strip EUR-Lex layout elements before markdown conversion.

    Removes XML processing instructions (e.g. <?xml version="1.0"?>).
    Removes script, style and noscript tags including their content entirely.
    Removes all <img> tags to prevent stray image paths in markdown output.
    Unwraps all table-related tags so their content flows as plain blocks.
    Removes <hr> tags that produce spurious horizontal rules in markdown.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove XML processing instructions
    for node in soup.find_all(string=lambda text: isinstance(text, ProcessingInstruction)):
        node.extract()

    # Completely remove script, style and noscript tags including inner content
    for tag in soup.find_all(["script", "style", "noscript"]):
        tag.decompose()

    # Remove all <img> tags — prevents stray file paths like europeanflag.gif in output
    for tag in soup.find_all("img"):
        tag.decompose()

    # Remove <hr> tags
    for hr in soup.find_all("hr"):
        hr.decompose()

    # Unwrap table structure tags
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
    Removes stray .fmx.xml filename lines.
    Strips trailing whitespace from each line.
    """
    cleaned_html = preprocess_html(html)
    raw = md(cleaned_html, heading_style="ATX")

    # Collapse 3+ consecutive newlines to one blank line
    result = re.sub(r"\n{3,}", "\n\n", raw)

    # Remove stray .fmx.xml filename lines
    result = re.sub(r"(?m)^.+\.fmx\.xml\s*$", "", result)

    # Remove EUR-Lex document header metadata  
    for pattern in [  
        r"(?m)^Amtsblatt der Europäischen Union\s*$",  
        r"(?m)^Official Journal of the European Union\s*$",  
        r"(?m)^(DE|EN)\s*$",  
        r"(?m)^(DE |EN )?(Reihe L|L series)\s*$",  
        r"(?m)^ISSN \d+-\d+ \(electronic edition\)\s*$",  
    ]:  
        result = re.sub(pattern, "", result)

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

    # Fix escaped underscores in URLs  
    result = re.sub(r"(?<=\S)\\_(?=\S)", "_", result)

    # Collapse again after removals to clean up leftover blank lines
    result = re.sub(r"\n{3,}", "\n\n", result)

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
source_de: "{SOURCES['de']}"
source_en: "{SOURCES['en']}"
date_fetched: {date.today().isoformat()}
languages:
        - DE
        - EN
tags:
created: {date.today().strftime("%Y-%m-%d %H:%M:%S")}
updated: {date.today().strftime("%Y-%m-%d %H:%M:%S")}
---

"""

note = (
    frontmatter
        + f"# {doc_title}\n\n"
        + "## 🇩🇪 - Deutsch\n\n"
        + content_de
        + "\n\n---\n\n"
        + "## 🇬🇧 - English\n\n"
        + content_en
)

OUTPUT_FILE.write_text(note, encoding="utf-8")
