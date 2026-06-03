#!/usr/bin/env python3
"""
Combined script:
  1. Rename UUID images → semantic names
  2. Update all HTML image references
  3. Fix FAQ double-fire bug
  4. Fix nav dropdown click (CSS + JS)
  5. Delete unreferenced images from /images/
"""
import os, glob, re

PROTO  = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'
IMAGES = os.path.join(PROTO, 'images')

# ── 1. Rename UUID images ─────────────────────────────────────────────────────
RENAMES = {
    '79441ac0-8f81-43f0-afa0-6791c80dcee5.jpeg': 'van-ge-jetdeau-pro.jpg',
    'f9d10ae1-f518-449a-a78c-ad0b829c2527.jpeg': 'van-vs-team.jpg',
    '15712d2a-0091-4433-ae21-e3fafb8645cb.jpeg': 'van-vs-alpes-grand.jpg',
    '1afc9a8c-915e-45f1-b1a1-1a62474997c0.jpeg': 'van-vs-montagne.jpg',
    '8fa0baa0-45f6-444c-81a6-cfed222e5605.jpeg': 'van-vs-sion-panorama.jpg',
    'f82aa58f-bb5d-4cb6-ab18-e24004d3c631.jpeg': 'van-vs-flotte.jpg',
    '8444edf3-5f0d-44d3-b827-c5f65b777589.jpeg': 'van-vs-noir.jpg',
    'fb665838-f4d2-4695-aad3-58f85ba9907d.jpeg': 'van-vs-vignes.jpg',
    '7eacc990-e52a-44ff-875b-ab83f1b4a51a.jpeg': 'van-vs-sion-2.jpg',
    'bffa71cf-0bcd-4c2f-b306-6252f87e3a30.jpeg': 'van-ju-delemont.jpg',
    '57832e47-958a-4408-ac51-f84fa0763f07.jpeg': 'van-vs-village.jpg',
}

print('=== 1. Renaming UUID images ===')
for old, new in RENAMES.items():
    src = os.path.join(IMAGES, old)
    dst = os.path.join(IMAGES, new)
    if os.path.exists(src):
        if os.path.exists(dst):
            os.remove(src)
            print(f'  SKIP (dst exists): {old[:8]}… → {new}')
        else:
            os.rename(src, dst)
            print(f'  {old[:8]}… → {new}')
    else:
        print(f'  NOT FOUND: {old}')

# ── 2. HTML image reference replacements ─────────────────────────────────────
GLOBAL = [
    ('van-ge-jetdeau-2.jpg',  'van-ge-jetdeau-pro.jpg'),
    ('van-ge-jetdeau-3.jpg',  'van-ge-jetdeau-pro.jpg'),
    ('van-ge-jetdeau.jpg',    'van-ge-jetdeau-pro.jpg'),
    ('van-vs-alpes.jpg',      'van-vs-sion-panorama.jpg'),
    ('van-flotte-duo.png',    'van-vs-team.jpg'),
    ('van-flotte-simple.png', 'van-ju-delemont.jpg'),
]

CANTON = {
    'vs-': [
        ('van-vs-chargement.jpg', 'van-vs-sion-panorama.jpg'),
        ('van-vs-sion.jpg',       'van-vs-sion-panorama.jpg'),
    ],
    'ge-': [
        ('van-ge-ems.jpg', 'van-ge-jetdeau-pro.jpg'),
    ],
    'ju-': [
        ('van-ju-place.jpg',        'van-ju-delemont.jpg'),
        ('van-ju-franches.jpg',     'van-ju-delemont.jpg'),
        ('van-ju-saintursanne.jpg', 'van-ju-delemont.jpg'),
    ],
    'fr-': [
        ('van-fr-cathedral.jpg', 'van-vs-village.jpg'),
        ('van-fr-fribourg.jpg',  'van-vs-village.jpg'),
        ('van-fr-gruyeres.jpg',  'van-vs-village.jpg'),
        ('van-fr-murten.jpg',    'van-vs-village.jpg'),
    ],
    'ne-': [
        ('van-ne-lac.jpg',     'van-vs-vignes.jpg'),
        ('van-ne-chateau.jpg', 'van-vs-vignes.jpg'),
        ('van-ne-chaux.jpg',   'van-vs-vignes.jpg'),
        ('van-ne-locle.jpg',   'van-vs-vignes.jpg'),
        ('van-ne-village.jpg', 'van-vs-vignes.jpg'),
    ],
    'vd-': [
        ('van-vd-chillon.jpg',   'van-vs-montagne.jpg'),
        ('van-vd-lac.jpg',       'van-vs-montagne.jpg'),
        ('van-vd-lavaux.jpg',    'van-vs-montagne.jpg'),
        ('van-vd-lavaux-2.jpg',  'van-vs-montagne.jpg'),
        ('van-vd-vevey.jpg',     'van-vs-montagne.jpg'),
        ('van-vd-chateau.jpg',   'van-vs-montagne.jpg'),
    ],
}

INDEX_SPECIFIC = [
    ('van-vd-chillon.jpg',    'van-ge-jetdeau-pro.jpg'),
    ('van-vd-lavaux.jpg',     'van-vs-sion-panorama.jpg'),
    ('van-fr-murten.jpg',     'van-vs-village.jpg'),
    ('van-vs-chargement.jpg', 'van-vs-montagne.jpg'),
]

# Also fix general landing pages (debarras-*.html, nettoyage-*.html)
GENERAL_PAGES_PREFIXES = [
    'debarras-', 'nettoyage-',
]
GENERAL_EXTRA = [
    ('van-vs-alpes.jpg',     'van-vs-sion-panorama.jpg'),
    ('van-ge-jetdeau.jpg',   'van-ge-jetdeau-pro.jpg'),
    ('van-flotte-duo.png',   'van-vs-team.jpg'),
    ('van-flotte-simple.png','van-ju-delemont.jpg'),
    ('van-vs-chargement.jpg','van-vs-sion-panorama.jpg'),
    ('van-vd-chillon.jpg',   'van-vs-montagne.jpg'),
    ('van-vd-lavaux.jpg',    'van-vs-sion-panorama.jpg'),
]

def apply(content, pairs):
    for old, new in pairs:
        content = content.replace(f'/images/{old}', f'/images/{new}')
        content = content.replace(f'val-debarras.ch/images/{old}',
                                  f'val-debarras.ch/images/{new}')
    return content

files   = glob.glob(os.path.join(PROTO, '*.html'))
updated = 0

print('\n=== 2. Updating HTML image references ===')
for path in sorted(files):
    fname = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    content = apply(content, GLOBAL)

    if fname == 'index.html':
        content = apply(content, INDEX_SPECIFIC)
    else:
        matched = False
        for prefix, pairs in CANTON.items():
            if fname.startswith(prefix):
                content = apply(content, pairs)
                matched = True
                break
        if not matched:
            for p in GENERAL_PAGES_PREFIXES:
                if fname.startswith(p):
                    content = apply(content, GENERAL_EXTRA)
                    break

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f'  {fname}')

print(f'  → {updated} files updated')

# ── 3. Fix FAQ double-fire ────────────────────────────────────────────────────
OLD_FAQ = """  document.querySelectorAll('.faq-section .faq-q').forEach(function(btn){
    if(btn.dataset.faqBound) return;
    btn.dataset.faqBound = '1';
    if(!btn.hasAttribute('aria-expanded')) btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click', function(e){ e.preventDefault(); toggleFaq(btn); });
    btn.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); toggleFaq(btn); }
    });
  });"""

NEW_FAQ = """  document.querySelectorAll('.faq-section .faq-q').forEach(function(btn){
    if(btn.dataset.faqBound) return;
    btn.dataset.faqBound = '1';
    if(!btn.hasAttribute('aria-expanded')) btn.setAttribute('aria-expanded','false');
    btn.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); toggleFaq(btn); }
    });
  });"""

# ── 4. Nav dropdown CSS + JS ──────────────────────────────────────────────────
OLD_HOVER = '.nav-item:hover .dd{opacity:1;visibility:visible;transform:translateY(0);}'
NEW_HOVER = (OLD_HOVER + '\n'
             '.nav-item.open .dd{opacity:1;visibility:visible;transform:translateY(0);}')

NAV_JS = """
<script>
/* Desktop nav dropdown — click toggle */
(function(){
  var navItems = document.querySelectorAll('#desktopNav .nav-item');
  if(!navItems.length) return;
  navItems.forEach(function(item){
    var btn = item.querySelector('.nav-btn');
    if(!btn) return;
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      var isOpen = item.classList.contains('open');
      navItems.forEach(function(i){ i.classList.remove('open'); });
      if(!isOpen) item.classList.add('open');
    });
  });
  document.addEventListener('click', function(){
    navItems.forEach(function(i){ i.classList.remove('open'); });
  });
})();
</script>
"""

f1 = f2css = f2js = 0

print('\n=== 3+4. Fixing FAQ + nav dropdowns ===')
for path in sorted(files):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    if OLD_FAQ in content:
        content = content.replace(OLD_FAQ, NEW_FAQ)
        f1 += 1

    if OLD_HOVER in content and '.nav-item.open .dd' not in content:
        content = content.replace(OLD_HOVER, NEW_HOVER)
        f2css += 1

    if 'Desktop nav dropdown' not in content and '#desktopNav' in content:
        content = content.replace('</body>', NAV_JS + '</body>')
        f2js += 1

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  {os.path.basename(path)}')

print(f'  → FAQ fix: {f1} | Nav CSS: {f2css} | Nav JS: {f2js}')

# ── 5. Delete unreferenced images ────────────────────────────────────────────
print('\n=== 5. Auditing image references ===')

# Collect all images referenced across all HTML files
referenced = set()
img_pattern = re.compile(r'/images/([^\s"\'<>?#]+)')

for path in glob.glob(os.path.join(PROTO, '*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for m in img_pattern.finditer(content):
        referenced.add(m.group(1))

print(f'  Referenced images: {len(referenced)}')
for r in sorted(referenced):
    print(f'    {r}')

# List all files in /images/
all_files = {os.path.basename(p) for p in glob.glob(os.path.join(IMAGES, '*'))}
print(f'\n  Total files in /images/: {len(all_files)}')

unreferenced = all_files - referenced
print(f'  Unreferenced: {len(unreferenced)}')
for u in sorted(unreferenced):
    print(f'    DELETE: {u}')

deleted = 0
for fname in unreferenced:
    fpath = os.path.join(IMAGES, fname)
    os.remove(fpath)
    deleted += 1

print(f'\n  → {deleted} files deleted')
print('\nAll done.')
