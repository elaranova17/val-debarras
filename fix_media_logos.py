#!/usr/bin/env python3
"""fix_media_logos.py — Replace RTS/20min text badges with real SVG logos"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
    'blog.html','blog-article-1.html',
]

# ── CSS: replace badge styles with logo styles ────────────────────
OLD_CSS = """.stat-media{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;}
.media-badge{
  padding:4px 12px;border-radius:6px;font-size:12px;font-weight:800;
}
.mb-rts{background:#e53e3e;color:white;}
.mb-20{background:#1a56db;color:white;}"""

NEW_CSS = """.stat-media{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;}
.media-logos-row{display:flex;align-items:center;gap:14px;}
.logo-media{
  filter:brightness(0) invert(1);
  opacity:.85;
  transition:opacity .2s;
  display:block;
}
.stat:hover .logo-media{opacity:1;}
.logo-rts{height:28px;width:auto;}
.logo-20min{height:20px;width:auto;}"""

# ── HTML: replace badge spans with img tags ───────────────────────
OLD_HTML = """      <div class="stat-n stat-media">
        <span class="media-badge mb-rts">RTS</span>
        <span class="media-badge mb-20">20min</span>
      </div>"""

NEW_HTML = """      <div class="stat-n stat-media media-logos-row">
        <img src="/images/logo-rts.svg" alt="RTS" class="logo-media logo-rts">
        <img src="/images/logo-20min.svg" alt="20 minutes" class="logo-media logo-20min">
      </div>"""

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)
    changes = []

    if OLD_CSS in html:
        html = html.replace(OLD_CSS, NEW_CSS, 1)
        changes.append('CSS logos')

    if OLD_HTML in html:
        html = html.replace(OLD_HTML, NEW_HTML, 1)
        changes.append('HTML logos')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_media_logos.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
