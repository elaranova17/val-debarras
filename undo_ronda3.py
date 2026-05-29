#!/usr/bin/env python3
"""undo_ronda3.py — Elimina testimonios, A+/A-, modo lectura y JS asociado"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'
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
    changes = []

    # 1. Eliminar bloque CSS TESTIMONIOS completo
    html = re.sub(
        r'/\* ══+\s*TESTIMONIOS\s*══+[^/]*/\* ══+\s*A\+ / A-[^/]*\.mode-btn\.active\{background:var\(--vert\);color:white;border-color:var\(--vert-fonce\);\}\s*@media[^}]+\{\.mode-btn\{display:none;\}\}',
        '',
        html,
        flags=re.DOTALL
    )

    # 2. Eliminar sección testimonios HTML
    html = re.sub(
        r'\n<!-- ============================================================ -->\n<!-- TESTIMONIOS.*?</section>\n',
        '\n',
        html,
        flags=re.DOTALL
    )

    # 3. Eliminar bloque A+/A- del header
    html = re.sub(
        r'\s*<div class="a11y-size">.*?</div>\n',
        '\n',
        html,
        flags=re.DOTALL
    )

    # 4. Eliminar JS de A+/A-
    html = re.sub(
        r'\n<script>\n// ── A\+ / A-.*?</script>',
        '',
        html,
        flags=re.DOTALL
    )

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}')
    else:
        print(f'  ~ {fname}: no change')

print('=== undo_ronda3.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
