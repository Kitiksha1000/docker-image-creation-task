#!/usr/bin/env python3
"""
Convert Markdown to styled HTML for PDF generation
"""

import re

def markdown_to_html(md_file, html_file):
    """Convert markdown to HTML with styling"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert headers
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    
    # Convert bold
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    
    # Convert code blocks
    content = re.sub(r'```json\n(.*?)\n```', r'<pre class="code-block"><code>\1</code></pre>', content, flags=re.DOTALL)
    content = re.sub(r'```(.*?)\n(.*?)\n```', r'<pre class="code-block"><code>\2</code></pre>', content, flags=re.DOTALL)
    
    # Convert inline code
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
    
    # Convert lists
    lines = content.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        # Numbered lists
        if re.match(r'^\d+\. ', line):
            if not in_list:
                html_lines.append('<ol>')
                in_list = 'ol'
            item = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', line)
            html_lines.append(item)
        # Bullet lists
        elif re.match(r'^- ', line) or re.match(r'^• ', line):
            if not in_list:
                html_lines.append('<ul>')
                in_list = 'ul'
            item = re.sub(r'^[-•] (.+)$', r'<li>\1</li>', line)
            html_lines.append(item)
        else:
            if in_list:
                html_lines.append(f'</{in_list}>')
                in_list = False
            html_lines.append(line)
    
    if in_list:
        html_lines.append(f'</{in_list}>')
    
    content = '\n'.join(html_lines)
    
    # Convert horizontal rules
    content = re.sub(r'^---$', r'<hr>', content, flags=re.MULTILINE)
    
    # Convert paragraphs (lines that aren't already HTML)
    lines = content.split('\n')
    html_lines = []
    for line in lines:
        if line.strip() and not line.strip().startswith('<') and not line.strip().endswith('>'):
            html_lines.append(f'<p>{line}</p>')
        else:
            html_lines.append(line)
    
    content = '\n'.join(html_lines)
    
    # Create full HTML document
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IMD API Agricultural Relevance Analysis</title>
    <style>
        @page {{
            margin: 2cm;
            size: A4;
        }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
            margin: 0;
            padding: 20px;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            font-size: 28px;
        }}
        
        h2 {{
            color: #34495e;
            border-left: 5px solid #3498db;
            padding-left: 15px;
            margin-top: 25px;
            font-size: 22px;
        }}
        
        h3 {{
            color: #2c3e50;
            margin-top: 20px;
            font-size: 18px;
        }}
        
        h4 {{
            color: #555;
            margin-top: 15px;
            font-size: 14px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 12px;
        }}
        
        th {{
            background: #34495e;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }}
        
        tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            color: #c7254e;
        }}
        
        pre.code-block {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 11px;
            line-height: 1.4;
        }}
        
        pre.code-block code {{
            background: transparent;
            color: #f8f8f2;
            padding: 0;
        }}
        
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        
        p {{
            margin: 10px 0;
        }}
        
        strong {{
            color: #2c3e50;
        }}
        
        .page-break {{
            page-break-after: always;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML file created: {html_file}")

if __name__ == "__main__":
    markdown_to_html("agricultural_relevance_analysis.md", "agricultural_relevance_analysis.html")
