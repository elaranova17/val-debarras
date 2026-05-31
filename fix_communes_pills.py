#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Communes couvertes: convierte la lista plana de texto (villes-list)
en pills/tags redondeados verdes, más legibles para adultos mayores.
Aplica a las 6 páginas de servicio. Idempotente.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
SERVICE_PAGES = [
    "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
]

PILLS_CSS = """
/* ===== Communes en pills ===== */
.communes-cloud{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:10px;}
.commune-pill{display:inline-block;padding:10px 20px;background:#f0fdf4;border:1.5px solid #009b74;border-radius:50px;font-size:.95rem;font-weight:500;color:#1a3d2e;transition:all .2s ease;}
.commune-pill:hover{background:#009b74;color:#fff;transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,155,116,.2);}
"""


def main():
    changed = []
    pat = re.compile(r'<div class="villes-list">(.*?)</div>', re.DOTALL)
    for page in SERVICE_PAGES:
        p = BASE / page
        html = p.read_text(encoding="utf-8")
        before = html

        m = pat.search(html)
        if m:
            raw = m.group(1)
            communes = [c.strip() for c in raw.split("·") if c.strip()]
            pills = "\n".join(
                f'      <span class="commune-pill">{c}</span>' for c in communes
            )
            cloud = '<div class="communes-cloud">\n' + pills + '\n    </div>'
            html = html[:m.start()] + cloud + html[m.end():]

        if '.communes-cloud{' not in html:
            html = html.replace('</style>', PILLS_CSS + '</style>', 1)

        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(page)

    print("Páginas modificadas:", ", ".join(changed) if changed else "ninguna")


if __name__ == "__main__":
    main()
