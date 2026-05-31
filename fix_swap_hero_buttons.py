#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Échange les boutons hero entre index.html (accueil) et les 6 pages ge-*.

- Accueil reçoit le design service : 3 boutons (téléphone + devis + nos services).
- Pages service reçoivent le design accueil : 2 boutons (appeler + devis long).

Ne touche qu'au contenu interne du premier .hero-btns dans <section class="hero">.
Idempotent.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent

SERVICE_PAGES = [
    "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
]

HOME_BTNS_INNER = """        <a href="tel:+41795805857" class="btn-phone"><svg class="icon icon-btn"><use href="#icon-phone-line"/></svg>079 580 58 57</a>
        <a href="#devis" class="btn-devis"><svg class="icon icon-btn"><use href="#icon-document-line"/></svg>Devis gratuit</a>
        <a href="#services" class="btn-services">Nos services →</a>"""

SERVICE_BTNS_INNER = """        <a href="tel:+41795805857" class="btn-phone"><svg class="icon icon-btn"><use href="#icon-phone-line"/></svg>Appeler maintenant</a>
        <a href="#devis" class="btn-devis"><svg class="icon icon-btn"><use href="#icon-document-line"/></svg>Demander un devis gratuit</a>"""

HERO_BTNS_PAT = re.compile(
    r'(<section class="hero">.*?<div class="hero-btns">)\s*.*?\s*(</div>)',
    re.DOTALL,
)


def replace_hero_btns(html, inner):
    m = HERO_BTNS_PAT.search(html)
    if not m:
        return html, False
    new = m.group(1) + "\n" + inner + "\n      " + m.group(2)
    return html[: m.start()] + new + html[m.end() :], True


def main():
    changed = []

    idx = (BASE / "index.html").read_text(encoding="utf-8")
    new_idx, ok = replace_hero_btns(idx, HOME_BTNS_INNER)
    if ok and new_idx != idx:
        (BASE / "index.html").write_text(new_idx, encoding="utf-8")
        changed.append("index.html")

    for page in SERVICE_PAGES:
        html = (BASE / page).read_text(encoding="utf-8")
        new_html, ok = replace_hero_btns(html, SERVICE_BTNS_INNER)
        if ok and new_html != html:
            (BASE / page).write_text(new_html, encoding="utf-8")
            changed.append(page)

    print("Pages modifiées:", ", ".join(changed) if changed else "aucune")


if __name__ == "__main__":
    main()
