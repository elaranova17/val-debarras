#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOTE 2a: bloque de contacto del formulario (fc-icon).
Reemplaza los emojis (📞 ✉️ ⚡ 📍) por iconos rellenos del sprite.
El cuadro pasa a fondo blanco para que el icono verde se lea bien. Idempotente.
"""
from pathlib import Path

BASE = Path(__file__).parent
PAGES = [
    "index.html", "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
]

FC_MAP = {
    '<div class="fc-icon">📞</div>': 'icon-phone',
    '<div class="fc-icon">✉️</div>': 'icon-email',
    '<div class="fc-icon">⚡</div>': 'icon-clock',
    '<div class="fc-icon">📍</div>': 'icon-map',
}

FC_CSS = (
    "/* fc-icon en sprite */"
    ".fc-icon{background:#fff !important;}"
    ".fc-icon .icon{width:22px;height:22px;color:#009b74;}"
)


def main():
    changed = []
    for page in PAGES:
        p = BASE / page
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        before = html
        for emoji_div, icon in FC_MAP.items():
            html = html.replace(
                emoji_div,
                f'<div class="fc-icon"><svg class="icon"><use href="#{icon}"/></svg></div>',
            )
        if '.fc-icon .icon{' not in html:
            html = html.replace('</style>', FC_CSS + '</style>', 1)
        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(page)
    print("Páginas modificadas:", ", ".join(changed) if changed else "ninguna")


if __name__ == "__main__":
    main()
