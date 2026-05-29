#!/usr/bin/env python3
"""
fix_form.py — Changements formulaire client
1. Formulaire à gauche, infos contact à droite (CSS order:-1 sur form-card)
2. Supprimer la ligne subtitle "Réponse sous 24h · Lundi–Samedi..."
3. Ajouter collage 3 photos sous les contacts
4. Moins de vert — fond section #1a1a1a (charcoal)
5. Meilleure visibilité pour personnes âgées (labels + inputs plus grands)
6. Fusionner Nom + Prénom → Nom complet sur les pages canton
"""
import re, os, glob

PATCH_CSS = """
/* ── PATCH form — formulaire gauche, charcoal, 3e âge ── */
.form-section{background:#1a1a1a !important;}
.form-card{order:-1 !important;}
.form-inner{grid-template-columns:1.1fr 1fr !important;}
.fl label{font-size:15px !important;font-weight:700 !important;color:rgba(255,255,255,.88) !important;margin-bottom:10px !important;letter-spacing:0 !important;}
.fl input,.fl select,.fl textarea{font-size:17px !important;min-height:54px !important;padding:15px 18px !important;line-height:1.5 !important;color:white !important;background:rgba(255,255,255,.10) !important;border:1.5px solid rgba(255,255,255,.22) !important;}
.fl textarea{min-height:110px !important;}
.form-card{background:rgba(255,255,255,.07) !important;border:1.5px solid rgba(255,255,255,.18) !important;}
.form-btn{font-size:18px !important;padding:18px 32px !important;letter-spacing:.3px;}
.form-info h2{font-size:34px !important;line-height:1.2 !important;}
.form-info-label{font-size:11px !important;color:rgba(255,255,255,.5) !important;}
.form-note{font-size:14px !important;color:rgba(255,255,255,.55) !important;margin-top:14px !important;}
.form-collage-3{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:22px;border-radius:10px;overflow:hidden;}
.form-collage-3 img{width:100%;height:88px;object-fit:cover;border-radius:7px;display:block;}
.fc-text{font-size:15.5px !important;}
.fc-text strong{font-size:16.5px !important;}
.fc-icon{width:44px !important;height:44px !important;font-size:20px !important;}
"""

COLLAGE_HTML = """      <div class="form-collage-3">
        <img src="/images/ge-action.jpg" alt="Intervention Genève">
        <img src="/images/vd-hero.jpg" alt="Débarras Vaud">
        <img src="/images/fr-hero.jpg" alt="Débarras Fribourg">
      </div>"""

TARGET_FILES = [
    'index.html',
    'ge-appartement.html', 'ge-maison.html', 'ge-succession.html',
    'ge-ems.html', 'ge-diogene.html', 'ge-nettoyage.html',
    'blog.html', 'blog-article-1.html',
]

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

def patch_file(fname):
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'  SKIP (not found): {fname}')
        return

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # ── 1. Inject CSS patch before </style> (first occurrence only) ──
    if PATCH_CSS.strip()[:20] not in html:
        html = html.replace('</style>', PATCH_CSS + '\n</style>', 1)

    # ── 2. Remove subtitle paragraph under h2 in form-info ──
    html = re.sub(
        r'\n?\s*<p>Réponse sous 24h · Lundi[–-]Samedi.*?</p>',
        '',
        html
    )

    # ── 3. Add collage after </div> closing form-contacts, if not already there ──
    if 'form-collage-3' not in html:
        # Match the closing of form-contacts div
        html = re.sub(
            r'(      </div>\n    </div>\n\n    <div class="form-card">)',
            COLLAGE_HTML + r'\n    </div>\n\n    <div class="form-card">',
            html,
            count=1
        )

    # ── 4. Canton pages: merge Nom + Prénom → Nom complet ──
    # Pattern: two adjacent Nom/Prénom fields in a form-row
    html = re.sub(
        r'<div class="form-row">\s*<div class="fl"><label>Nom \*</label><input type="text" placeholder="Nom"></div>\s*<div class="fl"><label>Prénom \*</label><input type="text" placeholder="Prénom"></div>\s*</div>',
        '<div class="form-row form-full" style="margin-bottom:16px">\n          <div class="fl"><label>Nom complet *</label><input type="text" placeholder="Prénom et nom" style="font-size:17px;min-height:54px;"></div>\n        </div>',
        html
    )

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ patched: {fname}')
    else:
        print(f'  ~ no change: {fname}')

print('=== fix_form.py ===')
for fname in TARGET_FILES:
    patch_file(fname)
print('Done.')
