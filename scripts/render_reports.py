#!/usr/bin/env python3
"""Render submission Markdown as standalone HTML with offline, printable tables."""
import html
from pathlib import Path
import re
import sys


def inline(value):
    token = re.compile(r'(!?\[[^\]]*\]\([^)]*\)|`[^`]+`|\*\*[^*]+\*\*)')
    out = []
    pos = 0
    for match in token.finditer(value):
        out.append(html.escape(value[pos:match.start()]))
        item = match.group(0)
        if item.startswith('`'):
            out.append('<code>' + html.escape(item[1:-1]) + '</code>')
        elif item.startswith('**'):
            out.append('<strong>' + html.escape(item[2:-2]) + '</strong>')
        else:
            image = item.startswith('!')
            label, target = re.fullmatch(r'!?\[([^\]]*)\]\(([^)]*)\)', item).groups()
            target = target.strip()
            if image:
                out.append('<img src="' + html.escape(target, quote=True) + '" alt="' + html.escape(label, quote=True) + '">')
            else:
                out.append('<a href="' + html.escape(target, quote=True) + '">' + html.escape(label) + '</a>')
        pos = match.end()
    out.append(html.escape(value[pos:]))
    return ''.join(out)


def render_markdown(markdown):
    lines = markdown.splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('```'):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            i += i < len(lines)
            blocks.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
            continue
        heading = re.match(r'^(#{1,6})\s+(.*)$', line)
        if heading:
            level = len(heading.group(1))
            blocks.append(f'<h{level}>' + inline(heading.group(2)) + f'</h{level}>')
            i += 1
            continue
        if line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|?\s*[-:| ]+\|?$', lines[i+1]):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(split_table_row(lines[i]))
                i += 1
            headers = rows[0]
            body = rows[2:]
            blocks.append('<div class="table-wrap"><table><thead><tr>' + ''.join('<th>' + inline(c) + '</th>' for c in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in row) + '</tr>' for row in body) + '</tbody></table></div>')
            continue
        if re.match(r'^\s*[-*]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*]\s+', lines[i]):
                item = re.sub(r'^\s*[-*]\s+', '', lines[i])
                check = re.match(r'^\[([ xX])\]\s+(.*)$', item)
                if check:
                    checked = ' checked' if check.group(1).lower() == 'x' else ''
                    item = '<input type="checkbox" disabled' + checked + '> ' + inline(check.group(2))
                else:
                    item = inline(item)
                items.append('<li>' + item + '</li>')
                i += 1
            blocks.append('<ul>' + ''.join(items) + '</ul>')
            continue
        if re.match(r'^\s*\d+\.\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append('<li>' + inline(re.sub(r'^\s*\d+\.\s+', '', lines[i])) + '</li>')
                i += 1
            blocks.append('<ol>' + ''.join(items) + '</ol>')
            continue
        if line.startswith('>'):
            quote = []
            while i < len(lines) and lines[i].startswith('>'):
                quote.append(inline(re.sub(r'^>\s?', '', lines[i])))
                i += 1
            blocks.append('<blockquote>' + '<br>'.join(quote) + '</blockquote>')
            continue
        if re.match(r'^\s*(---+|___+|\*\*\*+)\s*$', line):
            blocks.append('<hr>')
            i += 1
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('```', '#', '|', '>')) and not re.match(r'^\s*([-*]\s+|\d+\.\s+|---+\s*$)', lines[i]):
            paragraph.append(lines[i])
            i += 1
        blocks.append('<p>' + '<br>'.join(inline(part) for part in paragraph) + '</p>')
    return '\n'.join(blocks)


def split_table_row(line):
    """Split a Markdown table row without treating escaped or code-span pipes as separators."""
    value = line.strip()
    if value.startswith('|'):
        value = value[1:]
    if value.endswith('|') and not value.endswith('\\|'):
        value = value[:-1]
    cells, current = [], []
    in_code = False
    escaped = False
    for char in value:
        if char == '`' and not escaped:
            in_code = not in_code
        if char == '|' and not in_code and not escaped:
            cells.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == '\\' and not escaped
        if char != '\\':
            escaped = False
    cells.append(''.join(current).strip())
    return cells

STYLE = '''
:root{font-family:"Segoe UI",Arial,sans-serif;color:#17212b;background:#fff;line-height:1.65}
body{max-width:1200px;margin:36px auto;padding:0 26px 60px}
header{border-bottom:2px solid #17212b;padding-bottom:14px;margin-bottom:28px;color:#52606d}
h1{font-size:2rem;line-height:1.3}h2{margin-top:2.4rem;border-bottom:1px solid #dce1e6;padding-bottom:8px}
a{color:#164c88}.table-wrap{width:100%;overflow-x:auto;margin:20px 0}table{border-collapse:collapse;width:100%;min-width:680px;margin:0;font-size:.94rem}
th,td{border:1px solid #ccd2d8;padding:10px 12px;vertical-align:top;text-align:left;overflow-wrap:anywhere}th{background:#edf2f7}
tbody tr:nth-child(even){background:#f7f9fb}pre{background:#f3f5f7;padding:16px;white-space:pre-wrap;overflow-wrap:anywhere}
code{font-family:Consolas,"DejaVu Sans Mono",monospace;font-size:.9em}p,li,td{overflow-wrap:anywhere}
blockquote{margin:20px 0;padding:10px 20px;border-left:4px solid #52606d;background:#f5f7f9}
img{max-width:100%;height:auto;border:1px solid #dce1e6}
@media print{@page{size:A4;margin:16mm}body{margin:0;padding:0;font-size:10pt;max-width:none}header{display:none}
h1{font-size:19pt}h2{font-size:14pt;break-after:avoid}.table-wrap{overflow:visible}table{display:table;width:100%;min-width:0;table-layout:fixed;font-size:8pt}
th,td{padding:5px}thead{display:table-header-group}tr,figure{break-inside:avoid}a{color:#17212b}}
'''


def render(path):
    path = Path(path)
    markdown = path.read_text()
    title = next((line.lstrip('# ').strip() for line in markdown.splitlines() if line.startswith('# ')), path.stem)
    body = render_markdown(markdown)
    result = '<!doctype html>\n<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>' + html.escape(title) + '</title><style>' + STYLE + '</style></head><body><header>Weekly Report · ' + html.escape(title) + ' · <a href="' + html.escape(path.name, quote=True) + '">Bản Markdown để đọc/scan</a></header><main>' + body + '</main></body></html>\n'
    path.with_suffix('.html').write_text(result)


if __name__ == '__main__':
    for name in sys.argv[1:]:
        render(name)
