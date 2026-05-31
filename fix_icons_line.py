#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refonte du système d'icônes VD en LINE ICONS (style Lucide / Heroicons).
- Réécrit les définitions de <symbol> du sprite inline (#vd-icon-sprite) sur les 10 pages
- Réécrit le sprite autonome /icons/sprite.svg
- Garde EXACTEMENT les mêmes ids -> aucun changement de markup d'usage nécessaire
- Affine le bloc CSS "=== SISTEMA DE ICONOS VD ===" (transitions + animations subtiles au survol)
- Diogène : ajoute la classe icon-orange aux svg #icon-warning (home .sc-icon + pages .other-card-icon)
Idempotent : peut être relancé sans dupliquer ni casser.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
PAGES = [
    "index.html", "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
    "blog.html", "blog-article-1.html", "brand.html",
]

# Attributs communs Lucide pour le groupe enveloppant
G_OPEN = ('<g fill="none" stroke="currentColor" stroke-width="1.75" '
          'stroke-linecap="round" stroke-linejoin="round">')
G_CLOSE = "</g>"

# id -> contenu interne (formes), viewBox 0 0 24 24, tracés Lucide réels
SHAPES = {
    # téléphone (handset Lucide "phone") — même tracé pour les deux ids
    "icon-phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    # validation / avantages (Lucide "circle-check")
    "icon-check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    # appartement (Lucide "building-2")
    "icon-building": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    # maison (Lucide "home")
    "icon-house": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    # après décès / succession (Lucide "bird" — sobre et respectueux)
    "icon-dove": '<path d="M16 7h.01"/><path d="M3.4 18H12a8 8 0 0 0 8-8V7a4 4 0 0 0-7.28-2.3L2 20"/><path d="m20 7 2 .5-2 .5"/><path d="M10 18v3"/><path d="M14 17.75V21"/><path d="M7 18a6 6 0 0 0 3.84-10.61"/>',
    # EMS (bâtiment + croix médicale, sobre)
    "icon-hospital": '<path d="M3 21h18"/><path d="M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16"/><path d="M12 7v5"/><path d="M9.5 9.5h5"/>',
    # Diogène (Lucide "triangle-alert") — couleur orange gérée via CSS (.icon-orange)
    "icon-warning": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    # nettoyage extrême (Lucide "sparkles" — propreté, élégant)
    "icon-broom": '<path d="M12 3l1.9 5.8a2 2 0 0 0 1.3 1.3L21 12l-5.8 1.9a2 2 0 0 0-1.3 1.3L12 21l-1.9-5.8a2 2 0 0 0-1.3-1.3L3 12l5.8-1.9a2 2 0 0 0 1.3-1.3z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/>',
    # document (Lucide "file-text") — même tracé pour les deux ids
    "icon-document": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    # horloge (Lucide "clock")
    "icon-clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    # camion (Lucide "truck")
    "icon-truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    # localisation (Lucide "map-pin")
    "icon-map": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    # email (Lucide "mail")
    "icon-email": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    # étoile (Lucide "star" line)
    "icon-star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
}

# Les ids "-line" réutilisent le même tracé line
SHAPES["icon-phone-line"] = SHAPES["icon-phone"]
SHAPES["icon-document-line"] = SHAPES["icon-document"]

# Ordre stable (identique à l'existant)
ORDER = [
    "icon-phone", "icon-check", "icon-building", "icon-house", "icon-dove",
    "icon-hospital", "icon-warning", "icon-broom", "icon-document", "icon-clock",
    "icon-truck", "icon-map", "icon-email", "icon-star",
    "icon-phone-line", "icon-document-line",
]


def symbol(sid):
    return f'<symbol id="{sid}" viewBox="0 0 24 24">{G_OPEN}{SHAPES[sid]}{G_CLOSE}</symbol>'


SYMBOLS_XML = "".join(symbol(s) for s in ORDER)

INLINE_SPRITE = (
    '<svg id="vd-icon-sprite" aria-hidden="true" focusable="false" '
    'style="position:absolute;width:0;height:0;overflow:hidden">'
    + SYMBOLS_XML + '</svg>'
)

STANDALONE_SPRITE = (
    '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n  '
    + "\n  ".join(symbol(s) for s in ORDER)
    + "\n</svg>\n"
)

SPRITE_RE = re.compile(r'<svg id="vd-icon-sprite".*?</svg>', re.DOTALL)

# --- Nouveau bloc CSS du système d'icônes (line + animations subtiles) ---
NEW_CSS = (
    "/* === SISTEMA DE ICONOS VD === */"
    ".icon{width:24px;height:24px;flex-shrink:0;color:#009b74;display:inline-block;vertical-align:middle;transition:transform .2s ease,color .2s ease;}"
    ".icon-sm{width:16px;height:16px;}"
    ".icon-md{width:24px;height:24px;}"
    ".icon-lg{width:32px;height:32px;}"
    ".icon-xl{width:48px;height:48px;}"
    ".icon-green{color:#009b74;}"
    ".icon-orange{color:#f59e0b;}"
    ".icon-red{color:#ef4444;}"
    ".icon-white{color:#fff;}"
    ".sc-icon .icon{width:40px;height:40px;color:#009b74;}"
    ".sc-icon .icon-orange,.other-card-icon .icon-orange{color:#f59e0b;}"
    ".other-card-icon{color:#009b74;}"
    ".other-card:hover .other-card-icon .icon{transform:scale(1.08);}"
    ".icon-btn{width:1.05em;height:1.05em;color:inherit;flex-shrink:0;vertical-align:-0.16em;margin-right:.45em;display:inline-block;}"
    "/* fc-icon en sprite */.fc-icon{background:#fff !important;}.fc-icon .icon{width:22px;height:22px;color:#009b74;}"
    ".icon-ft{width:16px;height:16px;color:#22c55e;}"
)

# Remplace tout le bloc d'icônes : du marqueur jusqu'à juste avant </style>
CSS_RE = re.compile(r'/\* === SISTEMA DE ICONOS VD === \*/.*?(?=</style>)', re.DOTALL)

# Diogène orange : ajoute icon-orange aux svg warning (idempotent)
WARNING_OLD = '<svg class="icon"><use href="#icon-warning"/>'
WARNING_NEW = '<svg class="icon icon-orange"><use href="#icon-warning"/>'

# brand.html : cartes démo "Carte service (dark)" — remplace les emojis par le sprite line
SCD_MAP = {
    '<div class="scd-icon">🏠</div>': '<div class="scd-icon"><svg class="icon"><use href="#icon-building"/></svg></div>',
    '<div class="scd-icon">🏥</div>': '<div class="scd-icon"><svg class="icon"><use href="#icon-hospital"/></svg></div>',
    '<div class="scd-icon">🧹</div>': '<div class="scd-icon"><svg class="icon icon-orange"><use href="#icon-warning"/></svg></div>',
}


def main():
    (BASE / "icons").mkdir(exist_ok=True)
    (BASE / "icons" / "sprite.svg").write_text(STANDALONE_SPRITE, encoding="utf-8")
    print("icons/sprite.svg réécrit.")

    changed = []
    for page in PAGES:
        p = BASE / page
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        before = html

        # 1) Réécrit le sprite inline
        html = SPRITE_RE.sub(lambda _m: INLINE_SPRITE, html, count=1)

        # 2) Affine le bloc CSS d'icônes
        if CSS_RE.search(html):
            html = CSS_RE.sub(lambda _m: NEW_CSS, html, count=1)

        # 3) Diogène en orange (idempotent)
        html = html.replace(WARNING_OLD, WARNING_NEW)

        # 4) brand.html : cartes démo (emojis -> sprite line)
        if page == "brand.html":
            for old, new in SCD_MAP.items():
                html = html.replace(old, new)

        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(page)

    print("Pages modifiées :", ", ".join(changed) if changed else "aucune")


if __name__ == "__main__":
    main()
