#!/usr/bin/env python3
"""fix_logo.py — Add Val-Débarras name text next to logo image in all files"""
import os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
    'blog.html','blog-article-1.html',
]

OLD = '<a href="/" class="logo"><img src="/images/logo.jpg" alt="Val-Débarras" class="logo-img"></a>'
NEW = '<a href="/" class="logo"><img src="/images/logo.jpg" alt="Val-Débarras" class="logo-img"><div class="logo-text"><span class="logo-name">Val-Débarras</span><span class="logo-sub">Débarras &amp; nettoyage</span></div></a>'

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    if OLD in html:
        new_html = html.replace(OLD, NEW, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'  ✓ {os.path.basename(path)}')
    else:
        print(f'  ~ {os.path.basename(path)}: already updated or not found')

print('=== fix_logo.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
