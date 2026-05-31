#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guide design — Phase 1 : iconographie Lucide (stroke 1.5) + zéro emoji.

- Réécrit #vd-icon-sprite inline + /icons/sprite.svg (ids stables)
- Remplace les emojis par <use href="#icon-*"> (sauf bannière prototype 🟡)
- Idempotent : relançable sans effet de bord.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

G_OPEN = ('<g fill="none" stroke="currentColor" stroke-width="1.5" '
          'stroke-linecap="round" stroke-linejoin="round">')
G_CLOSE = "</g>"

SHAPES = {
    "icon-phone": (
        '<path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/>'
    ),
    "icon-check": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "icon-building": (
        '<path d="M10 12h4"/><path d="M10 8h4"/>'
        '<path d="M14 21v-3a2 2 0 0 0-4 0v3"/>'
        '<path d="M6 10H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2"/>'
        '<path d="M6 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16"/>'
    ),
    "icon-house": (
        '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/>'
        '<path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'
    ),
    "icon-dove": (
        '<path d="M19.414 14.414C21 12.828 22 11.5 22 9.5a5.5 5.5 0 0 0-9.591-3.676.6.6 0 0 1-.818.001A5.5 5.5 0 0 0 2 9.5c0 2.3 1.5 4 3 5.5l5.535 5.362a2 2 0 0 0 2.879.052 2.12 2.12 0 0 0-.004-3 2.124 2.124 0 1 0 3-3 2.124 2.124 0 0 0 3.004 0 2 2 0 0 0 0-2.828l-1.881-1.882a2.41 2.41 0 0 0-3.409 0l-1.71 1.71a2 2 0 0 1-2.828 0 2 2 0 0 1 0-2.828l2.823-2.762"/>'
    ),
    "icon-hospital": (
        '<path d="M11 2v2"/><path d="M5 2v2"/>'
        '<path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/>'
        '<path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>'
    ),
    "icon-warning": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
        '<path d="M12 8v4"/><path d="M12 16h.01"/>'
    ),
    "icon-broom": (
        '<path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"/>'
        '<path d="M20 2v4"/><path d="M22 4h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>'
    ),
    "icon-document": (
        '<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/>'
        '<path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M10 9H8"/>'
        '<path d="M16 13H8"/><path d="M16 17H8"/>'
    ),
    "icon-clock": ('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>'),
    "icon-truck": (
        '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/>'
        '<path d="M15 18H9"/>'
        '<path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/>'
        '<circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>'
    ),
    "icon-map": (
        '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/>'
        '<circle cx="12" cy="10" r="3"/>'
    ),
    "icon-email": (
        '<path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/>'
        '<rect x="2" y="4" width="20" height="16" rx="2"/>'
    ),
    "icon-star": (
        '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>'
    ),
    "icon-building-mgmt": (
        '<path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M12 6h.01"/>'
        '<path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M16 6h.01"/>'
        '<path d="M8 10h.01"/><path d="M8 14h.01"/><path d="M8 6h.01"/>'
        '<path d="M9 22v-3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v3"/>'
        '<rect x="4" y="2" width="16" height="20" rx="2"/>'
    ),
    "icon-clipboard-check": (
        '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>'
        '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
        '<path d="m9 14 2 2 4-4"/>'
    ),
    "icon-warehouse": (
        '<path d="M18 21V10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1v11"/>'
        '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 1.132-1.803l7.95-3.974a2 2 0 0 1 1.837 0l7.948 3.974A2 2 0 0 1 22 8z"/>'
        '<path d="M6 13h12"/><path d="M6 17h12"/>'
    ),
    "icon-arrow-up-narrow": (
        '<path d="m3 8 4-4 4 4"/><path d="M7 4v16"/>'
        '<path d="M11 12h4"/><path d="M11 16h7"/><path d="M11 20h10"/>'
    ),
    "icon-arrow-right": ('<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>'),
    "icon-shield-check": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "icon-chevron-down": ('<path d="m6 9 6 6 6-6"/>'),
    "icon-menu": ('<path d="M4 5h16"/><path d="M4 12h16"/><path d="M4 19h16"/>'),
    "icon-close": ('<path d="M18 6 6 18"/><path d="m6 6 12 12"/>'),
    "icon-message-circle": (
        '<path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719"/>'
    ),
    "icon-map-pin": (
        '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/>'
        '<circle cx="12" cy="10" r="3"/>'
    ),
    "icon-mountain": ('<path d="m8 3 4 8 5-5 5 15H2L8 3z"/>'),
    "icon-users": (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>'
        '<path d="M16 3.128a4 4 0 0 1 0 7.744"/>'
        '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/>'
    ),
    "icon-zap": (
        '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>'
    ),
    "icon-lock": (
        '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>'
        '<path d="M7 11V7a5 5 0 0 1 10 0v4"/>'
    ),
    "icon-calendar": (
        '<path d="M8 2v4"/><path d="M16 2v4"/>'
        '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>'
    ),
    "icon-shield": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>'
    ),
    "icon-palette": (
        '<path d="M12 22a1 1 0 0 1 0-20 10 9 0 0 1 10 9 5 5 0 0 1-5 5h-2.25a1.75 1.75 0 0 0-1.4 2.8l.3.4a1.75 1.75 0 0 1-1.4 2.8z"/>'
        '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/>'
        '<circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/>'
        '<circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/>'
        '<circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/>'
    ),
    "icon-car": (
        '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/>'
        '<circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>'
    ),
    "icon-folder-open": (
        '<path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/>'
    ),
    "icon-microscope": (
        '<path d="M6 18h8"/><path d="M3 22h18"/>'
        '<path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/>'
        '<path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/>'
        '<path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/>'
    ),
    "icon-church": (
        '<path d="M10 9h4"/><path d="M12 7v5"/>'
        '<path d="M14 21v-3a2 2 0 0 0-4 0v3"/>'
        '<path d="m18 9 3.52 2.147a1 1 0 0 1 .48.854V19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6.999a1 1 0 0 1 .48-.854L6 9"/>'
        '<path d="M6 21V7a1 1 0 0 1 .376-.782l5-3.999a1 1 0 0 1 1.249.001l5 4A1 1 0 0 1 18 7v14"/>'
    ),
    "icon-landmark": (
        '<path d="M10 18v-7"/>'
        '<path d="M11.119 2.205a2 2 0 0 1 1.762 0l7.84 3.846A.5.5 0 0 1 20.5 7h-17a.5.5 0 0 1-.22-.949z"/>'
        '<path d="M14 18v-7"/><path d="M18 18v-7"/><path d="M3 22h18"/><path d="M6 18v-7"/>'
    ),
    "icon-trees": (
        '<path d="M10 10v.2A3 3 0 0 1 8.9 16H5a3 3 0 0 1-1-5.8V10a3 3 0 0 1 6 0Z"/>'
        '<path d="M7 16v6"/><path d="M13 19v3"/>'
        '<path d="M12 19h8.3a1 1 0 0 0 .7-1.7L18 14h.2a1 1 0 0 0 .8-1.7L16 9h.2a1 1 0 0 0 .8-1.7L13 3l-1.4 1.5"/>'
    ),
    "icon-lightbulb": (
        '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>'
        '<path d="M9 18h6"/><path d="M10 22h4"/>'
    ),
}
SHAPES["icon-phone-line"] = SHAPES["icon-phone"]
SHAPES["icon-document-line"] = SHAPES["icon-document"]

SYMBOL_ORDER = [
    "icon-phone", "icon-check", "icon-building", "icon-house", "icon-dove",
    "icon-hospital", "icon-warning", "icon-broom", "icon-document", "icon-clock",
    "icon-truck", "icon-map", "icon-email", "icon-star", "icon-phone-line",
    "icon-document-line", "icon-building-mgmt", "icon-clipboard-check",
    "icon-warehouse", "icon-arrow-up-narrow", "icon-arrow-right", "icon-shield-check",
    "icon-chevron-down", "icon-menu", "icon-close", "icon-message-circle",
    "icon-map-pin", "icon-mountain", "icon-users", "icon-zap", "icon-lock",
    "icon-calendar", "icon-shield", "icon-palette", "icon-car", "icon-folder-open",
    "icon-microscope", "icon-church", "icon-landmark", "icon-trees", "icon-lightbulb",
]


def symbol_xml(sid):
    return f'<symbol id="{sid}" viewBox="0 0 24 24">{G_OPEN}{SHAPES[sid]}{G_CLOSE}</symbol>'


INLINE_SPRITE = (
    '<svg id="vd-icon-sprite" aria-hidden="true" focusable="false" '
    'style="position:absolute;width:0;height:0;overflow:hidden">'
    + "".join(symbol_xml(s) for s in SYMBOL_ORDER) + '</svg>'
)

STANDALONE_SPRITE = (
    '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n  '
    + "\n  ".join(symbol_xml(s) for s in SYMBOL_ORDER) + "\n</svg>\n"
)

ICON_CSS = """
/* === ICONOGRAPHIE GUIDE VD (Lucide 1.5) === */
.enc-icon,.pm-icon .icon,.hero-loc-icon .icon,.hbadge .icon,.trust-icon .icon{
  width:18px;height:18px;vertical-align:-3px;margin-right:4px;
}
.pm-icon .icon{width:28px;height:28px;margin:0;}
.enc-title{display:flex;align-items:flex-start;gap:8px;}
.enc-title .enc-icon{flex-shrink:0;margin-top:1px;}
.drawer-close .icon,.chev .icon,.arr .icon,.faq-arr .icon{width:14px;height:14px;display:inline-block;vertical-align:middle;}
"""

SPRITE_RE = re.compile(r'<svg id="vd-icon-sprite"[^>]*>.*?</svg>', re.DOTALL)
EMOJI_RE = re.compile(
    r'[\U0001F300-\U0001FAFF\U00002600-\U000027BF]'
    r'|[\U0001F1E0-\U0001F1FF]{2}|👨‍👩‍👧'
)

EMOJI_ICON = {
    "🏗️": "icon-building-mgmt", "🏗": "icon-building-mgmt",
    "🔑": "icon-clipboard-check", "🗝️": "icon-clipboard-check", "🗝": "icon-clipboard-check",
    "🏚️": "icon-warehouse", "🏚": "icon-warehouse", "🚐": "icon-arrow-up-narrow",
    "🚛": "icon-truck", "🚚": "icon-truck", "🏢": "icon-building",
    "🏔️": "icon-mountain", "🏔": "icon-mountain", "⭐": "icon-star",
    "📍": "icon-map-pin", "📋": "icon-document", "⚡": "icon-zap",
    "🔒": "icon-lock", "📅": "icon-calendar", "🇨🇭": "icon-shield",
    "🎨": "icon-palette", "🏠": "icon-house", "🏘️": "icon-house", "🏘": "icon-house",
    "🏥": "icon-hospital", "🕊️": "icon-dove", "🕊": "icon-dove",
    "⚰️": "icon-dove", "⚰": "icon-dove", "🚗": "icon-car",
    "🏛️": "icon-landmark", "🏛": "icon-landmark", "🚨": "icon-warning",
    "🔬": "icon-microscope", "🗂️": "icon-folder-open", "🗂": "icon-folder-open",
    "👴": "icon-users", "👨‍👩‍👧": "icon-users", "👨": "icon-users",
    "👩": "icon-users", "👧": "icon-users", "🤝": "icon-dove",
    "⛪": "icon-church", "🌲": "icon-trees", "💡": "icon-lightbulb",
    "✍️": "icon-document", "✍": "icon-document", "📐": "icon-document",
    "📦": "icon-warehouse", "🌅": "icon-zap", "⛈️": "icon-zap", "⛈": "icon-zap",
    "🍂": "icon-trees", "🏙️": "icon-building", "🏙": "icon-building",
    "🏴": "icon-shield", "🌙": "icon-star", "🌧️": "icon-zap", "🌧": "icon-zap",
    "🌉": "icon-landmark", "🚌": "icon-truck", "⚠️": "icon-warning", "⚠": "icon-warning",
}

FEATURE_TITLES = {
    "Immeuble et régie": "icon-building-mgmt",
    "État des lieux": "icon-clipboard-check",
    "Cave et dépendances": "icon-warehouse",
    "Accès difficile": "icon-arrow-up-narrow",
}


def svg_icon(icon_id, cls="icon icon-sm"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{icon_id}"/></svg>'


def process_html(html, fname):
    orig = html
    emoji_n = 0

    if SPRITE_RE.search(html):
        html = SPRITE_RE.sub(INLINE_SPRITE, html, count=1)

    if "ICONOGRAPHIE GUIDE VD" not in html:
        html = html.replace("</style>", ICON_CSS + "\n</style>", 1)

    for title, iid in FEATURE_TITLES.items():
        canonical = (
            f'<div class="enc-title">{svg_icon(iid, "icon icon-sm enc-icon")}'
            f'<span>{title}</span></div>'
        )
        html = re.sub(
            rf'<div class="enc-title">[^<]*{re.escape(title)}</div>',
            canonical, html,
        )

    for em, iid in {
        "🚛": "icon-truck", "🏢": "icon-building",
        "🏔️": "icon-mountain", "🏔": "icon-mountain", "⭐": "icon-star",
    }.items():
        html = html.replace(
            f'<span class="pm-icon">{em}</span>',
            f'<span class="pm-icon">{svg_icon(iid, "icon")}</span>',
        )

    html = re.sub(
        r'<span class="hbadge">✓\s*([^<]+)</span>',
        lambda m: f'<span class="hbadge">{svg_icon("icon-check", "icon icon-sm")} {m.group(1).strip()}</span>',
        html,
    )

    html = html.replace(
        "<span>📍</span>",
        f'<span class="hero-loc-icon">{svg_icon("icon-map-pin", "icon icon-sm")}</span>',
    )

    html = html.replace(
        '<button class="drawer-close" id="drawerClose">✕</button>',
        f'<button class="drawer-close" id="drawerClose" aria-label="Fermer">'
        f'{svg_icon("icon-close", "icon")}</button>',
    )

    chev_svg = svg_icon("icon-chevron-down", "icon")
    for cls in ("chev", "arr", "faq-arr"):
        html = html.replace(f'<span class="{cls}">▾</span>', f'<span class="{cls}">{chev_svg}</span>')

    if fname == "index.html":
        for em, iid in [
            ("📋", "icon-document"), ("⚡", "icon-zap"), ("🇨🇭", "icon-shield"),
            ("📍", "icon-map-pin"), ("🔒", "icon-lock"), ("📅", "icon-calendar"),
        ]:
            html = re.sub(
                rf'(<span style="width:32px;height:32px[^"]*">){re.escape(em)}(</span>)',
                rf'\1{svg_icon(iid, "icon trust-icon")}\2', html,
            )

    html = html.replace(
        '🎨 Charte',
        f'{svg_icon("icon-palette", "icon icon-sm")} Charte',
    )

    lines = []
    for line in html.split("\n"):
        if "🟡" in line and "NOUVEAU" in line:
            lines.append(line)
            continue

        def repl(m):
            nonlocal emoji_n
            ch = m.group(0)
            if ch == "🟡":
                return ch
            emoji_n += 1
            return svg_icon(EMOJI_ICON[ch], "icon icon-sm") if ch in EMOJI_ICON else ""

        lines.append(EMOJI_RE.sub(repl, line))
    html = "\n".join(lines)

    return html, html != orig, emoji_n


def main():
    (ROOT / "icons" / "sprite.svg").write_text(STANDALONE_SPRITE, encoding="utf-8")
    print("✓ icons/sprite.svg")

    changed, total_emoji = [], 0
    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        new, did, n = process_html(html, path.name)
        if did:
            path.write_text(new, encoding="utf-8")
            changed.append(path.name)
            total_emoji += n

    print(f"Pages modifiées : {len(changed)}")
    print(f"Emojis traités : {total_emoji}")


if __name__ == "__main__":
    main()
