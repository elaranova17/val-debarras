#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOTE 3: footer al sistema sprite.
- ft-phone-btn (bouton) -> icono de línea (regla de botones)
- contact email/phone + horaires clock -> iconos rellenos del sprite (verde)
Idempotente.
"""
from pathlib import Path

BASE = Path(__file__).parent
PAGES = [
    "index.html", "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
    "blog.html", "blog-article-1.html", "brand.html",
]

PHONE_PATH = ('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 '
              '19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 '
              '12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 '
              '2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>')

REPLACEMENTS = [
    # Bouton appel (footer) -> ligne
    (f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">{PHONE_PATH}</svg>',
     '<svg class="icon icon-btn"><use href="#icon-phone-line"/></svg>'),
    # Email (contact)
    ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
     '<svg class="icon icon-ft"><use href="#icon-email"/></svg>'),
    # Téléphone (contact)
    (f'<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" aria-hidden="true">{PHONE_PATH}</svg>',
     '<svg class="icon icon-ft"><use href="#icon-phone"/></svg>'),
    # Horaires (clock)
    ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>',
     '<svg class="icon icon-ft"><use href="#icon-clock"/></svg>'),
]

FT_CSS = ".icon-ft{width:16px;height:16px;color:#22c55e;}"


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
        if '.icon-ft{' not in html:
            html = html.replace('</style>', FT_CSS + '</style>', 1)
        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(page)
    print("Páginas modificadas:", ", ".join(changed) if changed else "ninguna")


if __name__ == "__main__":
    main()
