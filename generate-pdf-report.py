"""
Generate a PDF-ready HTML report from the Markdown report.
Replaces Mermaid code blocks with the pre-generated PNG images.

Usage:
    python generate-pdf-report.py

Output:
    docs/report/SEN3006_Report.html  (open in browser, Ctrl+P to save as PDF)
"""

import re
import base64
import os

REPORT_MD = os.path.join("docs", "report", "SEN3006_Task_Management_System_Report.md")
OUTPUT_HTML = os.path.join("docs", "report", "SEN3006_Report.html")
IMAGES_DIR = os.path.join("docs", "uml", "images")

# Map of mermaid diagram types to their PNG files
DIAGRAM_MAP = {
    "class-diagram": "class-diagram.png",
    "sequence-diagram": "sequence-diagram.png",
    "usecase-diagram": "usecase-diagram.png",
    "activity-diagram": "activity-diagram.png",
    "state-diagram": "state-diagram.png",
    "component-diagram": "component-diagram.png",
    "deployment-diagram": "deployment-diagram.png",
}


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def image_to_base64(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"


def replace_mermaid_with_images(md_content):
    """Replace ```mermaid ... ``` blocks with embedded PNG images."""
    diagram_index = [0]
    diagram_names = list(DIAGRAM_MAP.keys())

    def replacer(match):
        idx = diagram_index[0]
        if idx < len(diagram_names):
            name = diagram_names[idx]
            png_path = os.path.join(IMAGES_DIR, DIAGRAM_MAP[name])
            if os.path.exists(png_path):
                b64 = image_to_base64(png_path)
                diagram_index[0] += 1
                return f'<div class="diagram"><img src="{b64}" alt="{name}"></div>'
        diagram_index[0] += 1
        return match.group(0)

    return re.sub(r"```mermaid\n.*?```", replacer, md_content, flags=re.DOTALL)


def md_to_html(md_content):
    """Simple Markdown to HTML conversion (no external dependencies)."""
    lines = md_content.split("\n")
    html_lines = []
    in_code_block = False
    in_list = False
    in_table = False
    table_header_done = False

    for line in lines:
        # Code blocks
        if line.startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                lang = line[3:].strip()
                html_lines.append(f'<pre><code class="{lang}">')
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue

        # Horizontal rules
        if line.strip() == "---":
            html_lines.append("<hr>")
            continue

        # Headers
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = line.lstrip("#").strip()
            html_lines.append(f"<h{level}>{format_inline(text)}</h{level}>")
            continue

        # Tables
        if "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                table_header_done = True
                continue
            if not in_table:
                html_lines.append("<table>")
                in_table = True
            tag = "th" if not table_header_done else "td"
            row = "".join(f"<{tag}>{format_inline(c)}</{tag}>" for c in cells)
            html_lines.append(f"<tr>{row}</tr>")
            continue
        elif in_table:
            html_lines.append("</table>")
            in_table = False
            table_header_done = False

        # Unordered lists
        if re.match(r"^\s*[-*]\s", line):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            text = re.sub(r"^\s*[-*]\s", "", line)
            html_lines.append(f"<li>{format_inline(text)}</li>")
            continue
        # Ordered lists
        if re.match(r"^\s*\d+\.\s", line):
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
            text = re.sub(r"^\s*\d+\.\s", "", line)
            html_lines.append(f"<li>{format_inline(text)}</li>")
            continue
        elif in_list:
            html_lines.append("</ul>" if html_lines[-1] != "<ol>" else "</ol>")
            in_list = False

        # Empty lines
        if not line.strip():
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("")
            continue

        # Regular paragraph
        html_lines.append(f"<p>{format_inline(line)}</p>")

    if in_table:
        html_lines.append("</table>")
    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def format_inline(text):
    """Handle bold, italic, code, and links."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def wrap_html(body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SEN3006 - Task Management System Report</title>
<style>
    @page {{
        margin: 2.5cm;
        margin-top: 3cm;
        size: A4;
    }}
    body {{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #1a1a1a;
        max-width: 210mm;
        margin: 0 auto;
        padding: 2.5cm;
        padding-top: 3cm;
    }}
    h1 {{
        text-align: center;
        font-size: 16pt;
        margin-top: 2em;
        page-break-after: avoid;
    }}
    h2 {{
        font-size: 14pt;
        border-bottom: 1px solid #ccc;
        padding-bottom: 4px;
        margin-top: 2em;
        page-break-after: avoid;
    }}
    h3 {{
        font-size: 12pt;
        margin-top: 1.5em;
        page-break-after: avoid;
    }}
    p {{
        text-align: justify;
        margin: 0.5em 0;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        font-size: 10pt;
    }}
    th, td {{
        border: 1px solid #999;
        padding: 6px 10px;
        text-align: left;
    }}
    th {{
        background-color: #f0f0f0;
        font-weight: bold;
    }}
    pre {{
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        padding: 10px;
        font-size: 9pt;
        overflow-x: auto;
        line-height: 1.3;
        page-break-inside: avoid;
    }}
    code {{
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
    }}
    p code {{
        background-color: #f5f5f5;
        padding: 1px 4px;
        border-radius: 2px;
    }}
    .diagram {{
        text-align: center;
        margin: 1.5em 0;
        page-break-inside: avoid;
    }}
    .diagram img {{
        max-width: 100%;
        height: auto;
        border: 1px solid #ddd;
        border-radius: 4px;
    }}
    hr {{
        border: none;
        border-top: 1px solid #ccc;
        margin: 2em 0;
    }}
    ul, ol {{
        margin: 0.5em 0;
        padding-left: 2em;
    }}
    li {{
        margin: 0.3em 0;
    }}
    @media print {{
        body {{
            padding: 0;
        }}
        .diagram {{
            page-break-inside: avoid;
        }}
        pre {{
            page-break-inside: avoid;
        }}
    }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def main():
    print("Reading report...")
    md = read_file(REPORT_MD)

    print("Replacing Mermaid diagrams with PNG images...")
    md = replace_mermaid_with_images(md)

    print("Converting Markdown to HTML...")
    body = md_to_html(md)

    print("Wrapping in HTML document...")
    html = wrap_html(body)

    print(f"Writing to {OUTPUT_HTML}...")
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nDone! Open this file in your browser:")
    print(f"  {os.path.abspath(OUTPUT_HTML)}")
    print(f"\nThen press Ctrl+P -> 'Save as PDF' to create the final PDF.")
    print(f"Use these print settings:")
    print(f"  - Paper size: A4")
    print(f"  - Margins: Default or Minimum")
    print(f"  - Scale: 100% (or 90% if content overflows)")
    print(f"  - Background graphics: ON")


if __name__ == "__main__":
    main()
