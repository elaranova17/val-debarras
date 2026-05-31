#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETAPA 2: reemplaza el check ✓ por el icono SVG icon-check (cercle vert + check blanc)
únicamente sobre fondos claros: listes d'avantages (.av-check) + .sc-features du home.
Les badges du hero (fond vert foncé) restent en texte. Idempotente.
"""
from pathlib import Path

BASE = Path(__file__).parent
PAGES = [
    "index.html", "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
]

CHECK_SVG = '<svg class="icon icon-sm"><use href="#icon-check"/></svg>'

REPLACEMENTS = [
    # Listes d'avantages des pages service
    ('<span class="av-check">✓</span>', f'<span class="av-check">{CHECK_SVG}</span>'),
    # sc-features du home
    ('<li><span>✓</span>', f'<li><span>{CHECK_SVG}</span>'),
]


def main():
    changed = []
    for page in PAGES:
        p = BASE / page
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        before = html
        for old, new in REPLACEMENTS:
            html = html.replace(old, new)
        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(page)
    print("Páginas modificadas:", ", ".join(changed) if changed else "ninguna")


if __name__ == "__main__":
    main()
