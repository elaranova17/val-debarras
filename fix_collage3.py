#!/usr/bin/env python3
"""fix_collage3.py — Replace 4-image masonry with clean 3-image layout"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

NEW_CSS = """/* ══════════════════════════════════════════════════
   PHOTO MASONRY — 3 images formulaire
   ══════════════════════════════════════════════════ */
.photo-masonry{
  display:grid;
  grid-template-columns:1fr 1fr;
  grid-template-rows:1fr 1fr;
  gap:10px;
  margin-top:28px;
  height:280px;
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
.pm-cell--tall{grid-row:span 2;}"""

NEW_HTML = """<div class="photo-masonry">
        <!-- img1: gauche — tall, spans 2 rows -->
        <div class="pm-cell pm-cell--tall">
          <img src="/images/vd-fleet-dark.jpg" alt="Flotte Val-Débarras" loading="lazy">
          <div class="pm-overlay"><span class="pm-icon">🚛</span><span class="pm-label">Notre flotte</span></div>
        </div>
        <!-- img2: droite haut -->
        <div class="pm-cell">
          <img src="/images/ge-action.jpg" alt="Intervention Genève" loading="lazy">
          <div class="pm-overlay"><span class="pm-icon">🏢</span><span class="pm-label">Débarras urbain</span></div>
        </div>
        <!-- img3: droite bas -->
        <div class="pm-cell">
          <img src="/images/vd-hero.jpg" alt="Débarras Vaud" loading="lazy">
          <div class="pm-overlay"><span class="pm-icon">🏔️</span><span class="pm-label">Suisse romande</span></div>
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

    # 1. Replace masonry CSS block
    new_html = re.sub(
        r'/\* ══+\s*PHOTO MASONRY.*?\.pm-cell--wide\{[^}]+\}',
        NEW_CSS,
        html,
        count=1,
        flags=re.DOTALL
    )
    # fallback: also try without --wide rule if it was cleaned differently
    if new_html == html:
        new_html = re.sub(
            r'/\* ══+\s*PHOTO MASONRY.*?\.pm-cell--tall\{[^}]+\}',
            NEW_CSS,
            html,
            count=1,
            flags=re.DOTALL
        )
    if new_html != html:
        html = new_html
        changes.append('CSS 3img')

    # 2. Replace photo-masonry HTML block
    new_html2 = re.sub(
        r'<div class="photo-masonry">.*?</div>\s*</div>',
        NEW_HTML,
        html,
        count=1,
        flags=re.DOTALL
    )
    if new_html2 != html:
        html = new_html2
        changes.append('HTML 3img')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_collage3.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
