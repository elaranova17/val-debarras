#!/usr/bin/env python3
"""
fix_nav_names.py
1. Supprime le bouton WhatsApp flottant (HTML + CSS)
2. Ajoute un bouton "Retour en haut" avec scroll listener
3. Met à jour les noms dans la nav pour matcher le site officiel val-debarras.ch
4. Met à jour les titres des 6 cards service
"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

# ── Back-to-top CSS ──────────────────────────────────────────────
BACK_TO_TOP_CSS = """
/* ── Back to top button ── */
.back-to-top{
  position:fixed;bottom:24px;right:24px;z-index:200;
  width:48px;height:48px;border-radius:50%;
  background:var(--vert);color:white;border:none;cursor:pointer;
  font-size:20px;font-weight:700;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 4px 14px rgba(0,0,0,.22);
  transition:all .3s;opacity:0;visibility:hidden;transform:translateY(8px);
}
.back-to-top.visible{opacity:1;visibility:visible;transform:translateY(0);}
.back-to-top:hover{background:var(--vert-fonce);transform:translateY(-2px);}
"""

# ── Back-to-top HTML + JS (replace whatsapp button) ──────────────
BACK_TO_TOP_HTML = """<button class="back-to-top" id="backToTop" aria-label="Retour en haut de page" title="Retour en haut">↑</button>
<script>
(function(){
  var btn = document.getElementById('backToTop');
  if(!btn) return;
  window.addEventListener('scroll', function(){
    if(window.scrollY > 400) btn.classList.add('visible');
    else btn.classList.remove('visible');
  }, {passive:true});
  btn.addEventListener('click', function(){
    window.scrollTo({top:0, behavior:'smooth'});
  });
})();
</script>"""

# ── Nav button label replacements ────────────────────────────────
NAV_REPLACEMENTS = [
    ('Déb. appart. <span class="chev">▾</span>',
     'Débarras appartement <span class="chev">▾</span>'),
    ('Déb. maison <span class="chev">▾</span>',
     'Débarras maison <span class="chev">▾</span>'),
    ('Après décès <span class="chev">▾</span>',
     'Après décès/succession <span class="chev">▾</span>'),
    ('Entrée EMS <span class="chev">▾</span>',
     'Suite entrée EMS <span class="chev">▾</span>'),
    ('Diogène <span class="chev">▾</span>',
     'Insalubre/Diogène <span class="chev">▾</span>'),
    ('Nettoyage <span class="chev">▾</span>',
     'Nettoyages extrême <span class="chev">▾</span>'),
]

# ── Service card title replacements (index.html only) ────────────
CARD_REPLACEMENTS = [
    ('<div class="sc-title">Après décès &amp; succession</div>',
     '<div class="sc-title">Débarras après décès/succession</div>'),
    ('<div class="sc-title">Après décès & succession</div>',
     '<div class="sc-title">Débarras après décès/succession</div>'),
    ('<div class="sc-title">Entrée en EMS</div>',
     '<div class="sc-title">Débarras suite entrée EMS</div>'),
    ('<div class="sc-title">Diogène &amp; insalubre</div>',
     '<div class="sc-title">Débarras Insalubre/Diogène</div>'),
    ('<div class="sc-title">Diogène & insalubre</div>',
     '<div class="sc-title">Débarras Insalubre/Diogène</div>'),
    ('<div class="sc-title">Nettoyage extrême</div>',
     '<div class="sc-title">Nettoyages extrême</div>'),
    ('<div class="sc-title">Débarras appartement</div>',
     '<div class="sc-title">Débarras appartement</div>'),  # unchanged
    ('<div class="sc-title">Débarras maison</div>',
     '<div class="sc-title">Débarras maison</div>'),  # unchanged
]

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

    # 1. Remove WhatsApp CSS
    if '.whatsapp{' in html:
        html = re.sub(
            r'\.whatsapp\{[^}]+\}\s*\.whatsapp:hover\{[^}]+\}',
            '/* whatsapp removed */',
            html
        )
        changes.append('removed whatsapp CSS')

    # 2. Add back-to-top CSS (once)
    if 'Back to top button' not in html:
        html = html.replace('</style>', BACK_TO_TOP_CSS + '\n</style>', 1)
        changes.append('added back-to-top CSS')

    # 3. Replace WhatsApp anchor with back-to-top button + script
    if 'wa.me' in html:
        html = re.sub(
            r'<a href="https://wa\.me/[^"]*"[^>]*>.*?</a>',
            BACK_TO_TOP_HTML,
            html
        )
        changes.append('replaced whatsapp → back-to-top')

    # 4. Nav button label updates
    for old, new in NAV_REPLACEMENTS:
        if old in html:
            html = html.replace(old, new)
            changes.append(f'nav: {old[:20]}…')

    # 5. Service card title updates (all files — they may appear in related sections)
    for old, new in CARD_REPLACEMENTS:
        if old != new and old in html:
            html = html.replace(old, new)
            changes.append(f'card: {new[18:38]}')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_nav_names.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
