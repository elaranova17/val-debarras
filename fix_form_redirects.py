#!/usr/bin/env python3
"""
Update form onsubmit redirects from internal file paths
  window.location.href='/vs-appartement-merci.html'
to canonical URL paths
  window.location.href='/debarras-appartement/valais/merci/'
"""
import os

PROTO = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

CANTON = {
    'vs': 'valais',
    'vd': 'vaud',
    'ge': 'geneve',
    'fr': 'fribourg',
    'ne': 'neuchatel',
    'ju': 'jura',
}

SERVICE = {
    'appartement': 'debarras-appartement',
    'maison':      'debarras-maison',
    'succession':  'debarras-apres-deces-succession',
    'ems':         'debarras-ems',
    'diogene':     'debarras-insalubre-diogene',
    'nettoyage':   'nettoyage-extreme',
}

updated = 0
for canton_code, canton_slug in CANTON.items():
    for service_code, service_slug in SERVICE.items():
        fname = f'{canton_code}-{service_code}.html'
        fpath = os.path.join(PROTO, fname)
        if not os.path.exists(fpath):
            print(f'  MISSING: {fname}')
            continue

        old = f"window.location.href='/{canton_code}-{service_code}-merci.html'"
        new = f"window.location.href='/{service_slug}/{canton_slug}/merci/'"

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old in content:
            content = content.replace(old, new)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  {fname}  →  /{service_slug}/{canton_slug}/merci/')
            updated += 1
        else:
            # Try double-quote variant
            old2 = f'window.location.href="/{canton_code}-{service_code}-merci.html"'
            new2 = f'window.location.href="/{service_slug}/{canton_slug}/merci/"'
            if old2 in content:
                content = content.replace(old2, new2)
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'  {fname}  →  /{service_slug}/{canton_slug}/merci/')
                updated += 1
            else:
                print(f'  NO MATCH: {fname}')

print(f'\nDone — {updated}/36 files updated')
