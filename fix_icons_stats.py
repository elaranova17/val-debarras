#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOTE 2b: añade iconos a la barra de stats del home (fondo vert-dark).
clock (ans), building (logements), map (cantons), star (médias).
Iconos en verde claro para leerse sobre el fondo oscuro. Idempotente.
"""
from pathlib import Path

BASE = Path(__file__).parent
PAGE = BASE / "index.html"

def ic(icon):
    return f'<div class="stat-ic"><svg class="icon"><use href="#{icon}"/></svg></div>\n      '

INSERTS = [
    ('<div class="stat-n">+10</div>', ic("icon-clock") + '<div class="stat-n">+10</div>'),
    ('<div class="stat-n">500+</div>', ic("icon-building") + '<div class="stat-n">500+</div>'),
    ('<div class="stat-n">6</div>', ic("icon-map") + '<div class="stat-n">6</div>'),
    ('<div class="stat-n stat-media">', ic("icon-star") + '<div class="stat-n stat-media">'),
]

STATS_CSS = (
    "/* iconos stats */"
    ".stat-ic{display:flex;justify-content:center;margin-bottom:10px;}"
    ".stat-ic .icon{width:30px;height:30px;color:var(--vert-clair);}"
)


def main():
    html = PAGE.read_text(encoding="utf-8")
    before = html
    if '.stat-ic{' not in html:
        html = html.replace('</style>', STATS_CSS + '</style>', 1)
    for old, new in INSERTS:
        if 'stat-ic' not in html.split(old)[0][-120:]:  # evita doble inserción
            html = html.replace(old, new, 1)
    if html != before:
        PAGE.write_text(html, encoding="utf-8")
        print("index.html: stats con iconos.")
    else:
        print("Sin cambios (ya aplicado).")


if __name__ == "__main__":
    main()
