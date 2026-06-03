#!/usr/bin/env python3
import os, re, glob

PROTO = os.path.dirname(os.path.abspath(__file__))
files = [f for f in glob.glob(os.path.join(PROTO, '*.html')) if not f.endswith('brand.html')]

CHARTE = '      <a href="/brand" class="ft-bottom-link" style="color:#2e7d5c;"><svg class="icon icon-sm" aria-hidden="true"><use href="#icon-palette"/></svg> Charte</a>\n'

OLD_HERO_CTA = (
    '  /* 2 — Hero mobile : 1 bouton devis + lien téléphone texte */\n'
    '  .mobile-hero .hero-ctas {\n'
    '    flex-direction: column;\n'
    '    gap: 12px;\n'
    '    align-items: stretch;\n'
    '  }'
)
NEW_HERO_CTA = (
    '  /* 2 — Hero mobile : bouton masqué (sticky bar le remplace) */\n'
    '  .mobile-hero .hero-ctas {\n'
    '    display: none !important;\n'
    '  }'
)

fixed_charte = fixed_padding = fixed_cta = 0

for path in sorted(files):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # Fix 1 — Remove Charte link
    if CHARTE in content:
        content = content.replace(CHARTE, '')
        fixed_charte += 1

    # Fix 2 — padding-bottom 80px → 64px
    if 'padding-bottom:80px' in content:
        content = content.replace('padding-bottom:80px', 'padding-bottom:64px')
        fixed_padding += 1

    # Fix 3 — Hide mobile hero CTAs
    if OLD_HERO_CTA in content:
        content = content.replace(OLD_HERO_CTA, NEW_HERO_CTA)
        fixed_cta += 1

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  fixed: {os.path.basename(path)}')

print(f'\nDone — Charte: {fixed_charte}, padding: {fixed_padding}, hero CTA: {fixed_cta}')
