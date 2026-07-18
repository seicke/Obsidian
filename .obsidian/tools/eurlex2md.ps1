# --- Configuration ---  
$DOC_ID      = "L_202601778"  
$DATE_FETCHED = (Get-Date -Format "yyyy-MM-dd")

$SOURCES = @{  
    de = "https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=OJ:$DOC_ID"  
    en = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:$DOC_ID"  
}

$SCRIPT_DIR  = $PSScriptRoot  
$TARGET_DIR  = (Resolve-Path (Join-Path $SCRIPT_DIR "..\..\00 Inbox")).Path  
$OUTPUT_FILE = Join-Path $TARGET_DIR "$DOC_ID.md"

# --- Function: Fetch HTML and convert to Markdown via pandoc ---  
function Fetch-AsMarkdown {  
    param([string]$url)

    $response = Invoke-WebRequest -Uri $url -UseBasicParsing

    $tempHtml = [System.IO.Path]::ChangeExtension([System.IO.Path]::GetTempFileName(), ".html")  
    $tempMd   = [System.IO.Path]::ChangeExtension([System.IO.Path]::GetTempFileName(), ".md")

    [System.IO.File]::WriteAllText($tempHtml, $response.Content, [System.Text.Encoding]::UTF8)

    & pandoc -f html -t markdown_strict --markdown-headings=atx -o $tempMd $tempHtml

    $markdown = [System.IO.File]::ReadAllText($tempMd, [System.Text.Encoding]::UTF8)

    Remove-Item $tempHtml, $tempMd -ErrorAction SilentlyContinue

    return $markdown  
}

# --- Frontmatter ---  
$frontmatter = @"  
---  
title: "Verordnung $DOC_ID"  
aliases:  
        - "$DOC_ID"  
source_de: "$($SOURCES.de)"  
source_en: "$($SOURCES.en)"  
date_fetched: $DATE_FETCHED  
languages: [DE, EN]  
tags: [EU-Recht, Verordnung, bilingual]  
---

"@

# --- Fetch Content ---  
$contentDe = Fetch-AsMarkdown -url $SOURCES.de  
$contentEn = Fetch-AsMarkdown -url $SOURCES.en

# --- Assemble Note ---  
$note = $frontmatter +  
    "# Verordnung $DOC_ID`n`n" +  
    "## Deutsch`n`n" +  
    $contentDe +  
    "`n`n---`n`n" +  
    "## English`n`n" +  
    $contentEn

# --- Write Output (UTF-8 without BOM) ---  
[System.IO.File]::WriteAllText($OUTPUT_FILE, $note, [System.Text.Encoding]::UTF8)  
