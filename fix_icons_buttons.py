#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOTE 1 (botones): iconos de línea blanca en botones de color.
- Añade 2 símbolos de línea al sprite (icon-phone-line, icon-document-line)
- CSS .icon-btn (color:inherit -> toma el color del texto del botón)
- Reemplaza '📞 ' y '📋 ' (con espacio = solo botones) por el icono de línea
Idempotente.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
PAGES = [
    "index.html", "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
    "blog.html", "blog-article-1.html", "brand.html",
]

# Símbolos completos (14 base + 2 línea) — debe coincidir con fix_icons.py + líneas
SYMBOLS = {
    "icon-phone": '<rect x="4" y="2" width="16" height="20" rx="4" fill="currentColor"/><rect x="7" y="5" width="10" height="12" rx="1" fill="#fff"/><circle cx="12" cy="17" r="1.5" fill="#fff"/>',
    "icon-check": '<circle cx="12" cy="12" r="10" fill="currentColor"/><path d="M8 12l2.5 2.5L16 9" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "icon-building": '<rect x="3" y="3" width="18" height="18" rx="2" fill="currentColor"/><rect x="6" y="6" width="3" height="3" fill="#fff"/><rect x="15" y="6" width="3" height="3" fill="#fff"/><rect x="6" y="12" width="3" height="3" fill="#fff"/><rect x="15" y="12" width="3" height="3" fill="#fff"/><rect x="9" y="15" width="6" height="6" fill="#fff" opacity="0.3"/>',
    "icon-house": '<path d="M12 2L2 10h3v10h6v-6h2v6h6V10h3L12 2z" fill="currentColor"/><rect x="9" y="14" width="6" height="6" fill="#fff" opacity="0.3"/>',
    "icon-dove": '<circle cx="12" cy="12" r="8" fill="currentColor"/><path d="M8 10c-2 1-3 3-3 3s2-1 3-1c1 0 2 1 3 1s2-1 3-1c1 0 2 1 3 1s-1-2-3-3" fill="#fff" opacity="0.9"/><path d="M12 8v4" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>',
    "icon-hospital": '<rect x="4" y="3" width="16" height="18" rx="2" fill="currentColor"/><rect x="10" y="8" width="4" height="2" fill="#fff"/><rect x="11" y="6" width="2" height="6" fill="#fff"/><rect x="6" y="16" width="12" height="4" fill="#fff" opacity="0.3"/>',
    "icon-warning": '<path d="M12 3L2 20h20L12 3z" fill="#f59e0b"/><text x="12" y="17" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">!</text>',
    "icon-broom": '<rect x="11" y="2" width="2" height="12" rx="1" fill="#6b7280"/><rect x="6" y="14" width="12" height="6" rx="2" fill="currentColor"/><circle cx="8" cy="22" r="1" fill="#4ade80"/><circle cx="12" cy="23" r="1" fill="#4ade80"/><circle cx="16" cy="22" r="1" fill="#4ade80"/>',
    "icon-document": '<rect x="4" y="2" width="16" height="20" rx="2" fill="#fff" stroke="currentColor" stroke-width="2"/><line x1="7" y1="7" x2="17" y2="7" stroke="currentColor" stroke-width="1.5"/><line x1="7" y1="11" x2="17" y2="11" stroke="currentColor" stroke-width="1.5"/><line x1="7" y1="15" x2="12" y2="15" stroke="currentColor" stroke-width="1.5"/><circle cx="16" cy="16" r="3" fill="currentColor"/><path d="M14.5 16l1 1 2-2" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>',
    "icon-clock": '<circle cx="12" cy="12" r="10" fill="#fff" stroke="currentColor" stroke-width="2.5"/><line x1="12" y1="12" x2="12" y2="6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="12" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/>',
    "icon-truck": '<rect x="2" y="6" width="14" height="10" rx="2" fill="currentColor"/><rect x="16" y="8" width="6" height="8" rx="2" fill="#1a3d2e"/><circle cx="6" cy="18" r="2" fill="#374151"/><circle cx="18" cy="18" r="2" fill="#374151"/>',
    "icon-map": '<rect x="2" y="3" width="20" height="18" rx="2" fill="#e5e7eb"/><path d="M12 6c-3 0-5 2-5 5s5 9 5 9 5-6 5-9-2-5-5-5z" fill="currentColor"/><circle cx="12" cy="11" r="2" fill="#fff"/>',
    "icon-email": '<rect x="2" y="5" width="20" height="14" rx="2" fill="#fff" stroke="currentColor" stroke-width="2"/><path d="M2 7l10 6 10-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "icon-star": '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="#f59e0b"/>',
    # --- versiones de línea para botones (toman currentColor) ---
    "icon-phone-line": '<path d="M5 4h3l2 5-2.5 1.5a11 11 0 005 5L14 13l5 2v3a2 2 0 01-2 2A15 15 0 013 6a2 2 0 012-2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "icon-document-line": '<rect x="5" y="3" width="14" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="8.5" y1="8" x2="15.5" y2="8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="8.5" y1="12" x2="15.5" y2="12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="8.5" y1="16" x2="12.5" y2="16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
}

NEW_SPRITE = (
    '<svg id="vd-icon-sprite" aria-hidden="true" focusable="false" '
    'style="position:absolute;width:0;height:0;overflow:hidden">'
    + "".join(f'<symbol id="{s}" viewBox="0 0 24 24">{i}</symbol>'
              for s, i in SYMBOLS.items())
    + '</svg>'
)
SPRITE_RE = re.compile(r'<svg id="vd-icon-sprite".*?</svg>', re.DOTALL)

ICON_BTN_CSS = (
    ".icon-btn{width:1.05em;height:1.05em;color:inherit;flex-shrink:0;"
    "vertical-align:-0.16em;margin-right:.45em;display:inline-block;}"
)

PHONE_SVG = '<svg class="icon icon-btn"><use href="#icon-phone-line"/></svg>'
DOC_SVG = '<svg class="icon icon-btn"><use href="#icon-document-line"/></svg>'


def main():
    changed = []
    for page in PAGES:
        p = BASE / page
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        before = html

        # 1) Actualiza el sprite con los 2 iconos de línea
        html = SPRITE_RE.sub(lambda _m: NEW_SPRITE, html, count=1)

        # 2) CSS .icon-btn (idempotente)
        if '.icon-btn{' not in html:
            html = html.replace('</style>', ICON_BTN_CSS + '</style>', 1)

        # 3) Reemplazo solo en botones (emoji + espacio)
        html = html.replace('📞 ', PHONE_SVG)
        html = html.replace('📋 ', DOC_SVG)

        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(page)

    print("Páginas modificadas:", ", ".join(changed) if changed else "ninguna")


if __name__ == "__main__":
    main()
