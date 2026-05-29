#!/usr/bin/env python3
"""
fix_shields.py — Remplace tous les SVG clipPath complexes par des <img> simples
pointant vers les fichiers SVG officiels Wikipedia téléchargés en local.
"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

CANTON_NAMES = {
    'ge': 'Genève', 'vd': 'Vaud', 'vs': 'Valais',
    'fr': 'Fribourg', 'ne': 'Neuchâtel', 'ju': 'Jura'
}

# CSS patch — styles for the new clean SVG icons
CSS_PATCH = """
/* ── PATCH shields SVG — official Wikipedia vectors ── */
.canton-icon{object-fit:contain;flex-shrink:0;display:inline-block;filter:drop-shadow(0 1px 3px rgba(0,0,0,.18));}
.cpill .canton-icon{width:32px;height:40px;}
.dd a .canton-icon{width:22px;height:28px;}
.sidebar-card a .canton-icon{width:26px;height:32px;}
.canton-icon-breadcrumb{width:18px;height:22px;object-fit:contain;vertical-align:middle;margin-right:4px;}
"""

# Regex to match any of our custom clipPath SVG shields
# They all have viewBox="0 0 100 120" and contain href="/images/shield-XX.jpg"
SVG_RE = re.compile(
    r'<svg\s[^>]*?viewBox="0 0 100 120"[^>]*?>.*?</svg>',
    re.DOTALL
)

def replace_svg(match):
    svg_text = match.group(0)
    # Find canton code
    m = re.search(r'href="/images/shield-(\w+)\.jpg"', svg_text)
    if not m:
        return svg_text
    code = m.group(1)
    name = CANTON_NAMES.get(code, code.upper())
    return f'<img src="/images/shield-{code}.svg" class="canton-icon" alt="Écusson {name}" loading="lazy">'

def patch_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # 1. Replace all shield SVGs
    html, n = SVG_RE.subn(replace_svg, html)

    # 2. Fix breadcrumb SVG icon (different approach — small inline shield in breadcrumb)
    # These use the same pattern but may be in breadcrumb <li>
    # Already handled by the main regex above

    # 3. Inject CSS patch
    if 'PATCH shields SVG' not in html:
        html = html.replace('</style>', CSS_PATCH + '\n</style>', 1)

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {os.path.basename(path)}: {n} SVG blocks replaced')
    else:
        print(f'  ~ {os.path.basename(path)}: no change')

files = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
    'blog.html','blog-article-1.html',
]

print('=== fix_shields.py ===')
for fname in files:
    patch_file(os.path.join(BASE, fname))
print('Done.')
