#!/usr/bin/env python3
"""
Rename UUID images → semantic names and update all HTML references.
Assignment logic:
  VS pages  → van-vs-sion-panorama.jpg (hero)
  GE pages  → van-ge-jetdeau-pro.jpg
  JU pages  → van-ju-delemont.jpg
  FR pages  → van-vs-village.jpg (placeholder until FR photos taken)
  NE pages  → van-vs-vignes.jpg  (placeholder)
  VD pages  → van-vs-montagne.jpg (placeholder)
  index.html → van-ge-jetdeau-pro.jpg (hero)
"""
import os, glob

PROTO = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'
IMAGES = os.path.join(PROTO, 'images')

# ── 1. Rename UUID files ──────────────────────────────────────────────────────
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

print('=== Renaming images ===')
for old, new in RENAMES.items():
    src = os.path.join(IMAGES, old)
    dst = os.path.join(IMAGES, new)
    if os.path.exists(src):
        os.rename(src, dst)
        print(f'  {old[:8]}… → {new}')
    else:
        print(f'  NOT FOUND: {old}')

# ── 2. HTML replacements ──────────────────────────────────────────────────────

# Applied to ALL pages (gallery + og shared images)
GLOBAL = [
    ('van-ge-jetdeau-2.jpg',  'van-ge-jetdeau-pro.jpg'),
    ('van-ge-jetdeau-3.jpg',  'van-ge-jetdeau-pro.jpg'),
    ('van-ge-jetdeau.jpg',    'van-ge-jetdeau-pro.jpg'),
    ('van-vs-alpes.jpg',      'van-vs-sion-panorama.jpg'),
    ('van-flotte-duo.png',    'van-vs-team.jpg'),        # trabajadores (solicitado)
    ('van-flotte-simple.png', 'van-ju-delemont.jpg'),  # variedad Jura
]

# Per-canton hero replacements (applied only to files starting with prefix)
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

# index.html hero + media section (separate from canton logic)
INDEX_SPECIFIC = [
    ('van-vd-chillon.jpg',    'van-ge-jetdeau-pro.jpg'),
    ('van-vd-lavaux.jpg',     'van-vs-sion-panorama.jpg'),
    ('van-fr-murten.jpg',     'van-vs-village.jpg'),
    ('van-vs-chargement.jpg', 'van-vs-montagne.jpg'),
]


def apply(content, pairs):
    for old, new in pairs:
        content = content.replace(f'/images/{old}', f'/images/{new}')
        content = content.replace(f'val-debarras.ch/images/{old}',
                                  f'val-debarras.ch/images/{new}')
    return content


files = glob.glob(os.path.join(PROTO, '*.html'))
updated = 0

print('\n=== Updating HTML ===')
for path in sorted(files):
    fname = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    content = apply(content, GLOBAL)

    if fname == 'index.html':
        content = apply(content, INDEX_SPECIFIC)
    else:
        for prefix, pairs in CANTON.items():
            if fname.startswith(prefix):
                content = apply(content, pairs)
                break

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f'  {fname}')

print(f'\nDone — {updated} HTML files updated')
