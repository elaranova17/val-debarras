#!/usr/bin/env python3
"""fix_collage.py — Replace form-collage-3 with 4-image masonry photo grid"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

# ── New masonry CSS ───────────────────────────────────────────────
MASONRY_CSS = """
/* ══════════════════════════════════════════════════
   PHOTO MASONRY — 4 images formulaire
   ══════════════════════════════════════════════════ */
.photo-masonry{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:10px;
  margin-top:28px;
  border-radius:14px;
  overflow:hidden;
}
.pm-cell{
  position:relative;
  overflow:hidden;
  cursor:pointer;
  border-radius:10px;
}
.pm-cell img{
  width:100%;height:100%;
  object-fit:cover;
  transition:transform .5s cubic-bezier(.4,0,.2,1);
  display:block;
}
.pm-cell:hover img{transform:scale(1.08);}
.pm-overlay{
  position:absolute;inset:0;
  background:rgba(46,125,92,.85);
  opacity:0;
  transition:opacity .3s;
  display:flex;align-items:center;justify-content:center;
  flex-direction:column;color:#fff;gap:6px;
}
.pm-cell:hover .pm-overlay{opacity:1;}
.pm-icon{font-size:22px;}
.pm-label{font-weight:700;font-size:13px;letter-spacing:.3px;}
.pm-cell--sm{aspect-ratio:4/3;}
.pm-cell--tall{grid-row:span 2;aspect-ratio:auto;}
.pm-cell--wide{grid-column:span 2;aspect-ratio:16/9;}
"""

# ── New masonry HTML ──────────────────────────────────────────────
MASONRY_HTML = """<div class="photo-masonry">
        <!-- img1: top-left 4/3 -->
        <div class="pm-cell pm-cell--sm">
          <img src="/images/ge-action.jpg" alt="Intervention Genève" loading="lazy">
          <div class="pm-overlay"><span class="pm-icon">🏢</span><span class="pm-label">Débarras urbain</span></div>
        </div>
        <!-- img2: right tall, spans 2 rows -->
        <div class="pm-cell pm-cell--tall">
          <img src="/images/vd-fleet-dark.jpg" alt="Flotte Val-Débarras" loading="lazy">
          <div class="pm-overlay"><span class="pm-icon">🚛</span><span class="pm-label">Notre flotte</span></div>
        </div>
        <!-- img3: bottom-left 4/3 -->
        <div class="pm-cell pm-cell--sm">
          <img src="/images/vd-hero.jpg" alt="Débarras Vaud" loading="lazy">
          <div class="pm-overlay"><span class="pm-icon">🏔️</span><span class="pm-label">Suisse romande</span></div>
        </div>
        <!-- img4: wide bottom, spans 2 cols -->
        <div class="pm-cell pm-cell--wide">
          <img src="/images/fr-hero.jpg" alt="Débarras Fribourg" loading="lazy">
          <div class="pm-overlay"><span class="pm-icon">✅</span><span class="pm-label">Résultats garantis</span></div>
        </div>
      </div>"""

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
    'blog.html','blog-article-1.html',
]

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)
    changes = []

    # 1. Inject masonry CSS (replace old form-collage-3 CSS rule)
    if 'PHOTO MASONRY' not in html:
        # Remove old collage-3 CSS rule if present
        html = re.sub(
            r'\.form-collage-3\{[^}]+\}\s*\.form-collage-3 img\{[^}]+\}',
            '',
            html
        )
        html = html.replace('</style>', MASONRY_CSS + '\n</style>', 1)
        changes.append('CSS masonry')

    # 2. Replace form-collage-3 HTML block with masonry grid
    new_html = re.sub(
        r'<div class="form-collage-3">.*?</div>',
        MASONRY_HTML,
        html,
        count=1,
        flags=re.DOTALL
    )
    if new_html != html:
        html = new_html
        changes.append('masonry HTML')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_collage.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
