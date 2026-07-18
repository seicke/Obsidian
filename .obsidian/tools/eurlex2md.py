import requests
from markdownify import markdownify as md
from pathlib import Path
from datetime import date

SOURCES = {  
    "de": "https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=OJ:L_202601778",
    "en": "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202601778",
}

DOC_ID = "L_202601778"
OUTPUT_FILE = Path(f"{DOC_ID}.md")


def fetch_as_markdown(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return md(response.text, heading_style="ATX")


frontmatter = f"""---  
title: "Verordnung {DOC_ID}"
aliases:
    - "{DOC_ID}"
source_de: "{SOURCES['de']}"
source_en: "{SOURCES['en']}"
date_fetched: {date.today().isoformat()}
languages: [DE, EN]
tags: [EU-Recht, Verordnung, bilingual]
status: raw
---

"""

content_de = fetch_as_markdown(SOURCES["de"])
content_en = fetch_as_markdown(SOURCES["en"])

note = (
    frontmatter
        + f"# Verordnung {DOC_ID}\n\n"
        + "## 🇩🇪 Deutsch\n\n"
        + content_de
        + "\n\n---\n\n"
        + "## 🇬🇧 English\n\n"
        + content_en
)

OUTPUT_FILE.write_text(note, encoding="utf-8")