#!/usr/bin/env python3
"""fix_nav.py — 3 fixes:
  1. Remove menu-desc (canton city subtitles) from nav dropdowns
  2. Restore logo with name + subtitle text
  3. Center nav items between logo and CTA
"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
    'blog.html','blog-article-1.html',
]

# ── CSS patch ────────────────────────────────────────────────────
NAV_CSS_PATCH = """
/* ══════════════════════════════════════════════════
   NAV FIX — centrar + logo + sin desc cantons
   ══════════════════════════════════════════════════ */

/* Centro el nav entre logo y CTA */
.nav{justify-content:center !important;}

/* Ocultar desc cantons (seguridad por si queda alguno) */
.menu-desc{display:none !important;}

/* Simplificar altura dd ahora sin subtítulos */
.dd a{min-height:52px !important;padding:10px 14px !important;}

/* Logo: mostrar texto */
.logo-text{display:flex !important;flex-direction:column;}
.logo-name{font-size:16px !important;font-weight:800 !important;color:var(--gris-fonce) !important;}
.logo-sub{font-size:10px !important;color:var(--gris) !important;font-weight:500 !important;}
"""

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)
    changes = []

    # ── 1. Remove <span class="menu-desc">...</span> from dropdown links ──
    # Simplify: menu-text wrapper → just the menu-label text as plain <span>
    # From: <span class="menu-text"><span class="menu-label">Genève</span><span class="menu-desc">...</span></span>
    # To:   <span class="menu-label">Genève</span>
    new_html = re.sub(
        r'<span class="menu-text">(<span class="menu-label">[^<]+</span>)<span class="menu-desc">[^<]+</span></span>',
        r'\1',
        html
    )
    if new_html != html:
        html = new_html
        changes.append('menu-desc removed')

    # ── 2. Fix logo HTML: add text next to image (only if text not present) ──
    # Target the desktop header logo (not drawer)
    if 'logo-name' not in html:
        html = html.replace(
            '<a href="/" class="logo"><img src="/images/logo.jpg" alt="Val-Débarras" class="logo-img"></a>',
            '<a href="/" class="logo"><img src="/images/logo.jpg" alt="Val-Débarras" class="logo-img"><div class="logo-text"><span class="logo-name">Val-Débarras</span><span class="logo-sub">Débarras &amp; nettoyage</span></div></a>',
            1
        )
        if html != new_html:
            changes.append('logo text')

    # ── 3. Inject nav CSS patch ──
    if 'NAV FIX' not in html:
        html = html.replace('</style>', NAV_CSS_PATCH + '\n</style>', 1)
        changes.append('nav CSS')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_nav.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
