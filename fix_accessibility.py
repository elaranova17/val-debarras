#!/usr/bin/env python3
"""
fix_accessibility.py — Principios 3ª edad
1. CSS global: inputs 56px, fonts grandes, dropdowns 64px
2. Canton section index.html → canton-btn grande con escudo 48×60 + flecha
3. Nav dropdown: add .menu-desc sous chaque canton
"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

# ── Accessibility CSS Patch ───────────────────────────────────────
A11Y_CSS = """
/* ══════════════════════════════════════════════════
   ACCESSIBILITÉ 3E ÂGE — tailles, contrastes, espaces
   ══════════════════════════════════════════════════ */

/* Inputs & selects — 56px, 18px */
.fl input,.fl select,.fl textarea{
  font-size:18px !important;min-height:56px !important;
  padding:16px 18px !important;border-radius:12px !important;
}
.fl textarea{min-height:120px !important;}
.fl label{font-size:16px !important;font-weight:700 !important;margin-bottom:10px !important;}
.form-btn{font-size:20px !important;padding:20px 40px !important;min-height:60px !important;letter-spacing:.5px !important;width:100% !important;}

/* Nav dropdown — 64px par row, icône 32px, texte 16px */
.dd{min-width:260px !important;padding:10px !important;}
.dd a{
  min-height:64px !important;padding:12px 14px !important;
  gap:14px !important;align-items:center !important;border-radius:10px !important;
}
.dd a:hover{padding-left:18px !important;}
.dd .canton-icon{width:32px !important;height:40px !important;flex-shrink:0;}
.menu-text{display:flex;flex-direction:column;gap:2px;}
.menu-label{font-size:16px !important;font-weight:700;color:var(--gris-fonce);line-height:1.2;}
.menu-desc{font-size:12px;color:var(--gris);font-weight:400;line-height:1.3;}

/* Canton buttons — 80×60px minimum */
.canton-grid{display:flex;flex-wrap:wrap;justify-content:center;gap:16px;padding:8px 0;}
.canton-btn{
  display:flex;align-items:center;gap:16px;
  padding:16px 24px 16px 18px;
  min-height:72px;min-width:180px;
  background:white;border-radius:16px;
  box-shadow:0 2px 8px rgba(0,0,0,.08);
  border:1.5px solid #e5e7eb;
  transition:all .22s;
  text-decoration:none;
}
.canton-btn:hover{
  border-color:var(--vert);
  background:var(--vert-clair);
  transform:translateY(-3px);
  box-shadow:0 8px 24px rgba(46,125,92,.16);
}
.canton-btn__shield{width:40px;height:50px;object-fit:contain;flex-shrink:0;}
.canton-btn__info{display:flex;flex-direction:column;gap:2px;flex:1;}
.canton-btn__name{font-size:20px;font-weight:800;color:var(--gris-fonce);line-height:1.2;}
.canton-btn__sub{font-size:12px;color:var(--gris);font-weight:500;}
.canton-btn__arrow{font-size:20px;color:var(--vert);font-weight:700;margin-left:4px;transition:transform .2s;}
.canton-btn:hover .canton-btn__arrow{transform:translateX(4px);}

/* Général — espacement + lisibilité */
.sc-title{font-size:20px !important;}
.sc p,.bcard-excerpt{font-size:16px !important;line-height:1.7 !important;}
.section-h2{font-size:32px !important;}
.header-cta{font-size:16px !important;padding:12px 24px !important;min-height:52px !important;}
"""

# ── Canton descriptions per city ──────────────────────────────────
CANTON_CITIES = {
    'ge':  'Genève, Carouge, Meyrin, Lancy',
    'vd':  'Lausanne, Morges, Nyon, Yverdon',
    'vs':  'Sion, Martigny, Sierre, Monthey',
    'fr':  'Fribourg, Bulle, Estavayer',
    'ne':  'Neuchâtel, La Chaux-de-Fonds',
    'ju':  'Delémont, Porrentruy',
}
CANTON_NAMES = {
    'ge':'Genève','vd':'Vaud','vs':'Valais',
    'fr':'Fribourg','ne':'Neuchâtel','ju':'Jura'
}

# ── New canton section HTML for index.html ────────────────────────
def make_canton_grid():
    slug_map = {'ge':'geneve','vd':'vaud','vs':'valais','fr':'fribourg','ne':'neuchatel','ju':'jura'}
    items = []
    for code, name in CANTON_NAMES.items():
        cities = CANTON_CITIES[code]
        slug = slug_map[code]
        items.append(f'      <a href="/debarras-appartement/{slug}/" class="canton-btn">\n'
                     f'        <img src="/images/shield-{code}.svg" class="canton-btn__shield" alt="Écusson {name}" loading="lazy">\n'
                     f'        <span class="canton-btn__info">\n'
                     f'          <span class="canton-btn__name">{name}</span>\n'
                     f'          <span class="canton-btn__sub">{cities}</span>\n'
                     f'        </span>\n'
                     f'        <span class="canton-btn__arrow">→</span>\n'
                     f'      </a>')
    return '\n'.join(items)

NEW_CANTON_SECTION = f'''    <div class="canton-grid">
{make_canton_grid()}
    </div>'''

# ── Upgrade nav dropdown links with .menu-text + .menu-desc ──────
def upgrade_dd_links(html):
    """Add .menu-text + .menu-desc to each canton link in dropdowns."""
    slug_map = {'geneve':'ge','vaud':'vd','valais':'vs','fribourg':'fr','neuchatel':'ne','jura':'ju'}

    def replace_dd_link(m):
        full = m.group(0)
        # Skip if already upgraded
        if 'menu-label' in full:
            return full
        # Extract canton code from img src
        img_m = re.search(r'shield-(\w+)\.svg', full)
        if not img_m:
            return full
        code = img_m.group(1)
        name = CANTON_NAMES.get(code, code)
        cities = CANTON_CITIES.get(code, '')
        # Build new link: keep img, replace <span>Name</span> with menu-text block
        new = re.sub(
            r'<span>([^<]+)</span>',
            f'<span class="menu-text"><span class="menu-label">\\1</span><span class="menu-desc">{cities}</span></span>',
            full
        )
        return new

    # Match dropdown links (inside .dd)
    html = re.sub(
        r'<a href="[^"]*(?:debarras|nettoyage|succession|ems|diogene|insalubre)[^"]*">'
        r'<img[^>]+class="canton-icon"[^>]*>'
        r'<span>[^<]+</span></a>',
        replace_dd_link,
        html
    )
    return html

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
    'blog.html','blog-article-1.html',
]

def patch(path):
    with open(path,'r',encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)
    changes = []

    # 1. CSS patch
    if 'ACCESSIBILITÉ 3E ÂGE' not in html:
        html = html.replace('</style>', A11Y_CSS + '\n</style>', 1)
        changes.append('CSS a11y')

    # 2. Canton section → canton-btn (index.html only)
    if fname == 'index.html':
        old_pills = re.search(r'<div class="canton-pills">.*?</div>\s*</div>\s*</section>',
                              html, re.DOTALL)
        if old_pills and 'canton-btn' not in html:
            html = html.replace(
                '<div class="canton-pills">',
                '<!-- canton-pills replaced by canton-grid -->\n    <!--',
                1
            )
            # Simpler approach: replace the whole canton-pills div
            html = re.sub(
                r'<div class="canton-pills">.*?</div>',
                NEW_CANTON_SECTION,
                html,
                count=1,
                flags=re.DOTALL
            )
            changes.append('canton-grid')

    # 3. Upgrade nav dropdown links
    new_html = upgrade_dd_links(html)
    if new_html != html:
        html = new_html
        changes.append('dd links')

    if html != original:
        with open(path,'w',encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_accessibility.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
