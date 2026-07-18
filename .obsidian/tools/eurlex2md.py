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

    # ResponseBody returns raw bytes — decode explicitly to preserve UTF-8 characters  
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


def html_to_markdown(html: str) -> str:  
    """Convert HTML string to Markdown with ATX heading style."""  
    return md(html, heading_style="ATX")


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
languages: [DE, EN]  
tags: [EU-Recht, Verordnung, bilingual]  
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
