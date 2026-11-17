#!/usr/bin/env python3
"""Render the offline slide deck from editable JSON or build Reveal.js slides. No CDN, fonts or network requests."""
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    build_script = ROOT / 'scripts/build_reveal_slides.py'
    if build_script.exists():
        subprocess.run([sys.executable, str(build_script)], check=True)
        return

    # Fallback to legacy generator if build_script is absent
    slides = json.loads((ROOT/'slides/slides.json').read_text())

    sections = []
    for number, slide in enumerate(slides, 1):
        bullets = ''.join('<li>'+html.escape(item)+'</li>' for item in slide['bullets'])
        code = '<pre><code>'+html.escape(slide['code'])+'</code></pre>' if slide.get('code') else ''
        sections.append(f'<section class="slide" id="slide-{number}" aria-labelledby="title-{number}"'+(' hidden' if number > 1 else '')+f'><p class="stage">{html.escape(slide["stage"])}</p><h1 id="title-{number}">{html.escape(slide["title"])}</h1>{code}<ul>{bullets}</ul></section>')
    document = '''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Seminar · Unit Test, Coverage, CI/CD</title><link rel="icon" href="data:,">
<style>
:root { --paper:#fff; --ink:#101010; --muted:#4c4c4c; --rule:#d4d4d4; --code:#f4f4f4; }
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:"Segoe UI",Arial,sans-serif; }
header { display:flex; justify-content:space-between; gap:1rem; padding:1rem 4vw; border-bottom:1px solid var(--rule); font-size:.9rem; color:var(--muted); }
header strong { color:var(--ink); }
main { max-width:1440px; margin:auto; padding:4vh 6vw 7rem; }
.slide { min-height:70vh; }
.slide[hidden] { display:none; }
.stage { font-family:Consolas,"DejaVu Sans Mono",monospace; font-size:clamp(1rem,1.5vw,1.4rem); margin:0 0 2rem; color:var(--muted); }
h1 { font-family:Georgia,"DejaVu Serif",serif; font-size:clamp(2rem,4vw,4rem); line-height:1.14; letter-spacing:-.025em; margin:0 0 2.5rem; max-width:1100px; font-weight:normal; text-wrap:balance; }
ul { font-size:clamp(1.2rem,2.1vw,2rem); line-height:1.5; padding-left:1.2em; max-width:1140px; margin:0; }
li { padding-left:.25em; margin:.65em 0; }
pre { background:var(--code); border-left:5px solid var(--ink); padding:1.2rem 1.4rem; overflow:auto; font-size:clamp(.95rem,1.65vw,1.45rem); line-height:1.6; margin:0 0 1.7rem; }
code { font-family:Consolas,"DejaVu Sans Mono",monospace; }
nav { position:fixed; bottom:0; left:0; right:0; display:flex; align-items:center; gap:.8rem; background:var(--paper); border-top:1px solid var(--rule); padding:.8rem 4vw; }
button { min-height:44px; padding:.5rem 1rem; border:1px solid var(--ink); background:var(--paper); color:var(--ink); font:inherit; cursor:pointer; }
button:hover { background:var(--code); }
button:focus-visible { outline:3px solid var(--ink); outline-offset:3px; }
button:disabled { color:var(--muted); border-color:var(--rule); cursor:default; }
output { margin-left:auto; font-variant-numeric:tabular-nums; }
.hint { color:var(--muted); font-size:.85rem; }
@media(max-width:650px) { header span,.hint { display:none; } main { padding:2rem 6vw 6rem; } h1 { margin-bottom:1.5rem; } .stage { margin-bottom:1.2rem; } }
@media print { @page { size:landscape; margin:12mm; } header,nav { display:none; } main { padding:0; max-width:none; } .slide,.slide[hidden] { display:block!important; min-height:0; height:170mm; break-after:page; padding:6mm; } .slide:last-child { break-after:auto; } h1 { font-size:28pt; margin-bottom:12mm; } ul { font-size:19pt; line-height:1.35; } pre { font-size:14pt; white-space:pre-wrap; } .stage { font-size:12pt; margin-bottom:8mm; } }
</style></head><body>
<header><strong>Unit Test → Coverage → CI/CD</strong><span>Seminar · Tuần 06</span></header>
<main>'''+''.join(sections)+'''</main>
<nav aria-label="Điều khiển slide"><button id="prev" type="button">← Trước</button><button id="next" type="button">Tiếp →</button><span class="hint">Phím ← → · Ctrl+P để in</span><output id="counter" aria-live="polite"></output></nav>
<script>
const slides = Array.from(document.querySelectorAll('.slide'));
const prev = document.getElementById('prev');
const next = document.getElementById('next');
let index = 0;
function show(value) {
  index = Math.min(slides.length - 1, Math.max(0, value));
  slides.forEach((slide, i) => { slide.hidden = i !== index; });
  document.getElementById('counter').textContent = `${index + 1} / ${slides.length}`;
  prev.disabled = index === 0; next.disabled = index === slides.length - 1;
  history.replaceState(null, '', `#${index + 1}`);
  window.scrollTo(0, 0);
}
prev.addEventListener('click', () => show(index - 1));
next.addEventListener('click', () => show(index + 1));
document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || /INPUT|TEXTAREA|SELECT/.test(event.target.tagName)) return;
  if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') { event.preventDefault(); show(index + (event.key === 'ArrowRight' ? 1 : -1)); }
  if (event.key === 'Home') { event.preventDefault(); show(0); }
  if (event.key === 'End') { event.preventDefault(); show(slides.length - 1); }
});
const hashIndex = /^#[0-9]+$/.test(location.hash) ? Number(location.hash.slice(1)) - 1 : 0;
show(Number.isFinite(hashIndex) ? hashIndex : 0);
</script></body></html>'''
    (ROOT/'slides/index.html').write_text(document)
    print(f'Rendered {len(slides)} slides.')

if __name__ == '__main__':
    main()
