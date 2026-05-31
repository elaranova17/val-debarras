#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de iconos SVG uniforme para todo el sitio.
- Crea /icons/sprite.svg (referencia reutilizable)
- Inyecta el sprite inline (hidden) + CSS .icon en todas las páginas
- ETAPA 1: reemplaza los 6 iconos de servicio (home .sc-icon + pages .other-card-icon)
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

# ---- Definición de símbolos (id -> contenido interno, viewBox 0 0 24 24) ----
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
}

SYMBOLS_XML = "".join(
    f'<symbol id="{sid}" viewBox="0 0 24 24">{inner}</symbol>'
    for sid, inner in SYMBOLS.items()
)
INLINE_SPRITE = (
    '<svg id="vd-icon-sprite" aria-hidden="true" focusable="false" '
    'style="position:absolute;width:0;height:0;overflow:hidden">'
    + SYMBOLS_XML + '</svg>'
)

STANDALONE_SPRITE = (
    '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n  '
    + "\n  ".join(
        f'<symbol id="{sid}" viewBox="0 0 24 24">{inner}</symbol>'
        for sid, inner in SYMBOLS.items()
    )
    + "\n</svg>\n"
)

ICON_CSS = """
/* === SISTEMA DE ICONOS VD === */
.icon{width:24px;height:24px;flex-shrink:0;color:#009b74;display:inline-block;vertical-align:middle;}
.icon-sm{width:16px;height:16px;}
.icon-md{width:24px;height:24px;}
.icon-lg{width:32px;height:32px;}
.icon-xl{width:48px;height:48px;}
.icon-green{color:#009b74;}
.icon-orange{color:#f59e0b;}
.icon-red{color:#ef4444;}
.icon-white{color:#fff;}
.sc-icon .icon{width:40px;height:40px;color:#009b74;}
.other-card-icon{color:#009b74;}
"""

CSS_MARKER = "=== SISTEMA DE ICONOS VD ==="

SC_EMOJI_MAP = {
    "🏢": "icon-building", "🏡": "icon-house", "🕊️": "icon-dove",
    "🏥": "icon-hospital", "⚠️": "icon-warning", "🧹": "icon-broom",
}


def title_to_icon(title):
    t = title.lower()
    if "appartement" in t:
        return "icon-building"
    if "maison" in t:
        return "icon-house"
    if "décès" in t or "succession" in t:
        return "icon-dove"
    if "ems" in t:
        return "icon-hospital"
    if "diogène" in t or "insalubre" in t:
        return "icon-warning"
    if "nettoyage" in t:
        return "icon-broom"
    return "icon-document"


OTHER_CARD_RE = re.compile(
    r'(<div class="other-card-icon">)<svg viewBox="0 0 40 40".*?</svg>'
    r'(</div>\s*<h3 class="other-card-title">([^<]+)</h3>)',
    re.DOTALL,
)


def inject_foundation(html):
    if 'id="vd-icon-sprite"' not in html:
        html = re.sub(r'(<body[^>]*>)', r'\1\n' + INLINE_SPRITE, html, count=1)
    if CSS_MARKER not in html:
        html = html.replace('</style>', ICON_CSS + '</style>', 1)
    return html


def replace_sc_icons(html):
    for emoji, icon in SC_EMOJI_MAP.items():
        html = html.replace(
            f'<span class="sc-icon">{emoji}</span>',
            f'<span class="sc-icon"><svg class="icon"><use href="#{icon}"/></svg></span>',
        )
    return html


def replace_other_card_icons(html):
    def repl(m):
        icon = title_to_icon(m.group(3))
        return f'{m.group(1)}<svg class="icon"><use href="#{icon}"/></svg>{m.group(2)}'
    return OTHER_CARD_RE.sub(repl, html)


def main():
    (BASE / "icons").mkdir(exist_ok=True)
    (BASE / "icons" / "sprite.svg").write_text(STANDALONE_SPRITE, encoding="utf-8")

    changed = []
    for page in PAGES:
        p = BASE / page
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        before = html
        html = inject_foundation(html)
        html = replace_sc_icons(html)
        html = replace_other_card_icons(html)
        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(page)

    print("icons/sprite.svg escrito.")
    print("Páginas modificadas:", ", ".join(changed) if changed else "ninguna")


if __name__ == "__main__":
    main()
