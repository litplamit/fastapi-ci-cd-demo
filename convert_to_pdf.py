"""
Convert the FastAPI guide markdown to PDF
"""
import markdown2
from pathlib import Path

# Read the markdown file
md_file = Path(r"C:\Users\Amit_Jirange\.gemini\antigravity\brain\0b83aa23-19fe-4e56-baaa-74dc544296b7\fastapi_complete_guide.md")
output_html = Path(r"d:\Amit\MyFASTAPI\fastapi_complete_guide.html")

with open(md_file, 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Convert markdown to HTML with styling
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Complete FastAPI Application Guide</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #009688;
            border-bottom: 3px solid #009688;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #00796B;
            border-bottom: 2px solid #B2DFDB;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        h3 {{
            color: #00897B;
            margin-top: 25px;
        }}
        h4 {{
            color: #26A69A;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            line-height: 1.4;
        }}
        pre code {{
            background-color: transparent;
            color: #f8f8f2;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #009688;
            padding-left: 15px;
            margin-left: 0;
            color: #555;
            background-color: #f9f9f9;
            padding: 10px 15px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #009688;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .mermaid {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 5px 0;
        }}
        strong {{
            color: #00796B;
        }}
        a {{
            color: #009688;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .page-break {{
            page-break-after: always;
        }}
    </style>
</head>
<body>
{markdown2.markdown(markdown_content, extras=['fenced-code-blocks', 'tables', 'break-on-newline'])}
</body>
</html>
"""

# Write HTML file
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✓ HTML file created: {output_html}")
print("\nTo convert to PDF, you can:")
print("1. Open the HTML file in your browser")
print("2. Press Ctrl+P (Print)")
print("3. Select 'Save as PDF'")
print("4. Save to your desired location")
