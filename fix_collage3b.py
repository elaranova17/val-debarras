#!/usr/bin/env python3
"""fix_collage3b.py — Surgically replace full photo-masonry block (incl. leftover cells)"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

# Match the entire photo-masonry div + anything before the closing form-info </div>
# anchor on the known structure that follows: </div>\n\n    <div class="form-card">
NEW_MASONRY = '''      <div class="photo-masonry">
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
      </div>
    </div>'''

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
]

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)

    # Match from <div class="photo-masonry"> all the way to the last </div>
    # before <div class="form-card"> (which closes form-info)
    new_html = re.sub(
        r'<div class="photo-masonry">.*?</div>\s*</div>(?=\s*\n\s*<div class="form-card">)',
        NEW_MASONRY,
        html,
        count=1,
        flags=re.DOTALL
    )

    if new_html != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'  ✓ {fname}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_collage3b.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
