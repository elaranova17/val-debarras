#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refonte des icônes de service (jeu line Lucide, viewBox 0 0 24 24, stroke 1.75).
Réécrit 3 définitions de <symbol> jugées peu lisibles, sur les 10 pages
(sprite inline #vd-icon-sprite) + le sprite autonome /icons/sprite.svg.

Les ids restent STABLES -> aucun changement du markup d'usage (<use href>).

Choix (ancien -> nouveau, tracé Lucide authentique) :
  - icon-dove     : Lucide "bird" (lisait bizarrement) -> Lucide "flower-2"
                    (lys, connotation funéraire sobre)        [après décès / succession]
  - icon-hospital : croix dans un cadre (générique)    -> Lucide "bed"
                    (lit médicalisé, lisible « maison de retraite ») [entrée EMS]
  - icon-broom    : Lucide "sparkles" (décoratif)      -> Lucide "spray-can"
                    (produit/aérosol, sens « nettoyage » clair)     [nettoyage extrême]

Inchangés (déjà propres) : icon-building (building-2), icon-house (home),
icon-warning (triangle-alert, orange via .icon-orange).

Idempotent : relançable, réécrit chaque symbole ciblé à sa valeur canonique.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
PAGES = [
    "index.html", "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
    "blog.html", "blog-article-1.html", "brand.html",
]

G_OPEN = ('<g fill="none" stroke="currentColor" stroke-width="1.75" '
          'stroke-linecap="round" stroke-linejoin="round">')
G_CLOSE = "</g>"

# id -> tracés (Lucide réels, normalisés viewBox 0 0 24 24)
NEW_SHAPES = {
    # après décès / succession — Lucide "flower-2" (lys, sobre et digne)
    "icon-dove": (
        '<path d="M12 5a3 3 0 1 1 3 3m-3-3a3 3 0 1 0-3 3m3-3v1M9 8a3 3 0 1 0 3 3M9 8h1m5 0a3 3 0 1 1-3 3m3-3h-1m-2 3v-1"/>'
        '<circle cx="12" cy="8" r="2"/>'
        '<path d="M12 10v12"/>'
        '<path d="M12 22c4.2 0 7-1.667 7-5-4.2 0-7 1.667-7 5Z"/>'
        '<path d="M12 22c-4.2 0-7-1.667-7-5 4.2 0 7 1.667 7 5Z"/>'
    ),
    # entrée EMS — Lucide "bed" (lit médicalisé / maison de retraite)
    "icon-hospital": (
        '<path d="M2 4v16"/>'
        '<path d="M2 8h18a2 2 0 0 1 2 2v10"/>'
        '<path d="M2 17h20"/>'
        '<path d="M6 8v9"/>'
    ),
    # nettoyage extrême — Lucide "spray-can" (sens « nettoyage » clair)
    "icon-broom": (
        '<path d="M3 3h.01"/>'
        '<path d="M7 5h.01"/>'
        '<path d="M11 7h.01"/>'
        '<path d="M3 7h.01"/>'
        '<path d="M7 9h.01"/>'
        '<path d="M3 11h.01"/>'
        '<rect width="4" height="4" x="15" y="5"/>'
        '<path d="m19 9 2 2v10c0 .6-.4 1-1 1h-6c-.6 0-1-.4-1-1V11l2-2"/>'
        '<path d="m13 14 8-2"/>'
        '<path d="m13 19 8-2"/>'
    ),
}


def canonical_symbol(sid):
    return (f'<symbol id="{sid}" viewBox="0 0 24 24">'
            f'{G_OPEN}{NEW_SHAPES[sid]}{G_CLOSE}</symbol>')


def replace_symbol(html, sid):
    """Remplace tout le <symbol id="sid" ...>...</symbol> par sa version canonique."""
    pattern = re.compile(rf'<symbol id="{re.escape(sid)}"[^>]*>.*?</symbol>', re.DOTALL)
    return pattern.sub(lambda _m: canonical_symbol(sid), html, count=1)


def process(text):
    for sid in NEW_SHAPES:
        text = replace_symbol(text, sid)
    return text


def main():
    changed = []
    for page in PAGES:
        p = BASE / page
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        new = process(html)
        if new != html:
            p.write_text(new, encoding="utf-8")
            changed.append(page)

    sprite = BASE / "icons" / "sprite.svg"
    if sprite.exists():
        svg = sprite.read_text(encoding="utf-8")
        new = process(svg)
        if new != svg:
            sprite.write_text(new, encoding="utf-8")
            changed.append("icons/sprite.svg")

    print("Fichiers modifiés :", ", ".join(changed) if changed else "aucun")


if __name__ == "__main__":
    main()
