#!/usr/bin/env python3
"""fix_logo2.py — Fix logo size: bigger, not cropped, name larger"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

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

    # 1. Fix the crop override block (height:28px / object-fit:cover / object-position)
    html = re.sub(
        r'(\.logo-img\{)\s*width:[^;]+;\s*height:[^;]+;\s*object-fit:cover[^;]+;\s*object-position:[^;]+;\s*border-radius:[^;]+;\s*background:[^}]+\}',
        r'.logo-img{width:58px !important;height:58px !important;object-fit:contain !important;border-radius:8px !important;background:white !important;}',
        html
    )
    if html != original:
        changes.append('logo-img crop fix')

    # 2. Update base logo-img rule
    html = re.sub(
        r'\.logo-img\{width:46px;height:46px;object-fit:contain;border-radius:6px;background:white;\}',
        '.logo-img{width:58px;height:58px;object-fit:contain;border-radius:8px;background:white;}',
        html
    )

    # 3. Update logo-name and logo-sub in NAV FIX block
    html = re.sub(
        r'(\.logo-name\{font-size:)16px( !important;font-weight:800 !important;color:var\(--gris-fonce\) !important;\})',
        r'\g<1>20px\2',
        html
    )
    html = re.sub(
        r'(\.logo-sub\{font-size:)10px( !important;)',
        r'\g<1>11.5px\2',
        html
    )

    # 4. Update base logo-name rule
    html = re.sub(
        r'(\.logo-name\{font-size:)17px(;font-weight:800;)',
        r'\g<1>20px\2',
        html
    )
    html = re.sub(
        r'(\.logo-sub\{font-size:)10\.5px(;)',
        r'\g<1>11.5px\2',
        html
    )

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_logo2.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
