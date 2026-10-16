#!/usr/bin/env python3
"""Render submission Markdown as standalone HTML with offline, printable tables."""
import html
from pathlib import Path
import sys
from markdown_it import MarkdownIt

STYLE = '''
:root{font-family:"Segoe UI",Arial,sans-serif;color:#17212b;background:#fff;line-height:1.65}
body{max-width:1200px;margin:36px auto;padding:0 26px 60px}
header{border-bottom:2px solid #17212b;padding-bottom:14px;margin-bottom:28px;color:#52606d}
h1{font-size:2rem;line-height:1.3}h2{margin-top:2.4rem;border-bottom:1px solid #dce1e6;padding-bottom:8px}
a{color:#164c88}table{border-collapse:collapse;width:100%;display:block;overflow-x:auto;margin:20px 0;font-size:.94rem}
th,td{border:1px solid #ccd2d8;padding:10px 12px;vertical-align:top;text-align:left}th{background:#edf2f7}
tbody tr:nth-child(even){background:#f7f9fb}pre{background:#f3f5f7;padding:16px;white-space:pre-wrap;overflow-wrap:anywhere}
code{font-family:Consolas,"DejaVu Sans Mono",monospace;font-size:.9em}p,li,td{overflow-wrap:anywhere}
blockquote{margin:20px 0;padding:10px 20px;border-left:4px solid #52606d;background:#f5f7f9}
img{max-width:100%;height:auto;border:1px solid #dce1e6}
@media print{@page{size:A4;margin:16mm}body{margin:0;padding:0;font-size:10pt;max-width:none}header{display:none}
h1{font-size:19pt}h2{font-size:14pt;break-after:avoid}table{display:table;table-layout:fixed;font-size:8pt}
th,td{padding:5px}thead{display:table-header-group}tr,figure{break-inside:avoid}a{color:#17212b}}
'''


def render(path):
    path = Path(path)
    markdown = path.read_text()
    title = next((line.lstrip('# ').strip() for line in markdown.splitlines() if line.startswith('# ')), path.stem)
    body = MarkdownIt('commonmark', {'html': False}).enable('table').render(markdown)
    result = '<!doctype html>\n<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>' + html.escape(title) + '</title><style>' + STYLE + '</style></head><body><header>Weekly Report · Tuần thực hành 04 · <a href="' + html.escape(path.name, quote=True) + '">Bản Markdown để đọc/scan</a></header><main>' + body + '</main></body></html>\n'
    path.with_suffix('.html').write_text(result)


if __name__ == '__main__':
    for name in sys.argv[1:]:
        render(name)
