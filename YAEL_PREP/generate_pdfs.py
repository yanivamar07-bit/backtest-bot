#!/usr/bin/env python3
"""Convert YAEL prep markdown files to styled PDFs."""

import os
import markdown
from weasyprint import HTML, CSS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "PDF")
os.makedirs(PDF_DIR, exist_ok=True)

# RTL-aware CSS — supports Hebrew + French side by side
STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@400;700&family=Open+Sans:wght@400;600;700&display=swap');

@page {
    size: A4;
    margin: 18mm 15mm 20mm 15mm;
    @bottom-center {
        content: "YAEL — Programme de préparation | Page " counter(page) " / " counter(pages);
        font-size: 9pt;
        color: #888;
        font-family: 'Open Sans', sans-serif;
    }
}

body {
    font-family: 'Open Sans', 'Noto Sans Hebrew', 'DejaVu Sans', Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.6;
    color: #222;
    background: white;
}

/* Title page header */
h1 {
    font-size: 20pt;
    font-weight: 700;
    color: #1a3a5c;
    border-bottom: 3px solid #1a3a5c;
    padding-bottom: 8px;
    margin-top: 24px;
    margin-bottom: 16px;
    page-break-before: auto;
}

h2 {
    font-size: 14pt;
    font-weight: 700;
    color: #1a6b8a;
    border-left: 4px solid #1a6b8a;
    padding-left: 10px;
    margin-top: 20px;
    margin-bottom: 10px;
}

h3 {
    font-size: 12pt;
    font-weight: 600;
    color: #2e7d32;
    margin-top: 16px;
    margin-bottom: 8px;
}

h4 {
    font-size: 11pt;
    font-weight: 600;
    color: #555;
    margin-top: 12px;
    margin-bottom: 6px;
}

p {
    margin: 6px 0 8px 0;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

thead tr {
    background-color: #1a3a5c;
    color: white;
}

thead th {
    padding: 7px 10px;
    text-align: left;
    font-weight: 600;
}

tbody tr:nth-child(even) {
    background-color: #f0f4f8;
}

tbody tr:nth-child(odd) {
    background-color: #ffffff;
}

tbody td {
    padding: 5px 10px;
    border-bottom: 1px solid #dde3ea;
    vertical-align: top;
}

/* Blockquotes = tips / notes */
blockquote {
    background: #fffde7;
    border-left: 4px solid #f9a825;
    margin: 10px 0;
    padding: 8px 14px;
    border-radius: 0 4px 4px 0;
    font-size: 9.5pt;
    color: #444;
}

blockquote p { margin: 2px 0; }

/* Code blocks = visual cards / frames */
pre {
    background: #f5f7fa;
    border: 1px solid #c8d0dc;
    border-radius: 6px;
    padding: 12px 14px;
    font-family: 'Courier New', 'DejaVu Sans Mono', monospace;
    font-size: 9pt;
    white-space: pre-wrap;
    page-break-inside: avoid;
    line-height: 1.5;
}

code {
    background: #eef2f7;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 9pt;
    font-family: 'Courier New', monospace;
}

/* Lists */
ul, ol {
    margin: 6px 0 10px 0;
    padding-left: 22px;
}

li {
    margin-bottom: 4px;
}

/* Horizontal rule = section separator */
hr {
    border: none;
    border-top: 2px solid #e0e6ed;
    margin: 16px 0;
}

/* Hebrew text direction hint */
[lang="he"], .he {
    direction: rtl;
    unicode-bidi: embed;
    font-family: 'Noto Sans Hebrew', 'DejaVu Sans', Arial, sans-serif;
}

/* Strong / bold */
strong {
    color: #1a3a5c;
}

/* Checkboxes in task lists */
input[type="checkbox"] {
    margin-right: 6px;
}

/* Page break control */
h1, h2 { page-break-after: avoid; }
table, pre, blockquote { page-break-inside: avoid; }

/* Cover banner per file */
.cover-banner {
    background: linear-gradient(135deg, #1a3a5c 0%, #1a6b8a 100%);
    color: white;
    padding: 20px 24px;
    border-radius: 8px;
    margin-bottom: 20px;
}
.cover-banner h1 { color: white; border-bottom-color: rgba(255,255,255,0.4); }
.cover-banner p { color: rgba(255,255,255,0.85); font-size: 10pt; }
"""

FILES = [
    ("README.md",                    "00_YAEL_Overview"),
    ("01_evaluation_initiale.md",    "01_Evaluation_Initiale"),
    ("02_programme_30_jours.md",     "02_Programme_30_Jours"),
    ("03_vocabulaire_1000_mots.md",  "03_Vocabulaire_1000_Mots"),
    ("04_connecteurs_logiques.md",   "04_Connecteurs_Logiques"),
    ("05_exercices_quotidiens.md",   "05_Exercices_Quotidiens"),
    ("06_methode_reponses_rapides.md","06_Methode_Reponses"),
    ("07_methode_redaction.md",      "07_Methode_Redaction"),
    ("08_examens_blancs.md",         "08_Examens_Blancs"),
    ("09_analyse_erreurs.md",        "09_Analyse_Erreurs"),
    ("10_fiches_revision.md",        "10_Fiches_Revision"),
    ("11_corriges_detailles.md",     "11_Corriges_Detailles"),
]

MD_EXT = markdown.Markdown(extensions=["tables", "fenced_code", "nl2br", "sane_lists"])

def md_to_html(md_path, title):
    with open(md_path, encoding="utf-8") as f:
        raw = f.read()
    MD_EXT.reset()
    body = MD_EXT.convert(raw)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{title}</title>
</head>
<body>
<div class="cover-banner">
  <p style="margin:0 0 4px 0; font-size:9pt; opacity:0.7">Programme YAEL — 30 jours pour atteindre 100</p>
  <p style="margin:0; font-size:14pt; font-weight:700">{title.replace("_", " ")}</p>
</div>
{body}
</body>
</html>"""

css = CSS(string=STYLE)

for md_name, pdf_name in FILES:
    md_path = os.path.join(BASE_DIR, md_name)
    pdf_path = os.path.join(PDF_DIR, f"{pdf_name}.pdf")
    if not os.path.exists(md_path):
        print(f"  SKIP (not found): {md_name}")
        continue
    print(f"  Generating {pdf_name}.pdf ...", end=" ", flush=True)
    html_str = md_to_html(md_path, pdf_name)
    HTML(string=html_str, base_url=BASE_DIR).write_pdf(pdf_path, stylesheets=[css])
    size_kb = os.path.getsize(pdf_path) // 1024
    print(f"OK ({size_kb} KB)")

print(f"\nDone — PDFs saved in: {PDF_DIR}")
