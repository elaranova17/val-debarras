#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Navbar desktop — menu sur une ligne (≥1025px) + chevrons dropdown visibles.

Idempotent : relançable sans effet de bord.
Cible tous les *.html du dossier prototype.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKER = "NAVBAR LAYOUT v1"

NAVBAR_CSS = """
/* === NAVBAR LAYOUT v1 — une ligne desktop + chevrons === */
@media(min-width:1025px){
  .header-inner{gap:8px;padding:0 14px;}
  .logo{margin-right:0;gap:8px;}
  .logo-img{width:50px;}
  .logo-name{font-size:17px !important;}
  .logo-sub{font-size:10px !important;}
  .nav{
    flex:1 1 auto;min-width:0;
    flex-wrap:nowrap !important;
    justify-content:flex-start !important;
    gap:0;
  }
  .nav-btn{
    font-size:11.5px;
    padding:7px 5px;
    gap:4px;
    letter-spacing:-0.03em;
  }
  .header-cta{
    font-size:12.5px !important;
    padding:8px 12px !important;
    min-height:auto !important;
    gap:5px !important;
  }
  .header-cta .icon-btn{width:18px !important;height:18px !important;}
}
.nav-btn .chev{
  font-size:inherit;
  display:inline-flex;
  align-items:center;
  line-height:1;
  transition:transform .2s;
}
.nav-chevron{
  width:14px;height:14px;
  opacity:.9;
  color:#64748b;
  flex-shrink:0;
  transition:transform .2s,color .2s;
}
.nav-item:hover .nav-chevron{color:#009b74;}
.nav-item:hover .chev{transform:rotate(180deg);}
.nav-item.open .nav-chevron{transform:rotate(180deg);}
"""

CHEV_OLD = (
    '<span class="chev"><svg class="icon" aria-hidden="true">'
    '<use href="#icon-chevron-down"/></svg></span>'
)
CHEV_NEW = (
    '<span class="chev"><svg class="icon icon-sm nav-chevron" aria-hidden="true">'
    '<use href="#icon-chevron-down"/></svg></span>'
)

# Text chevrons legacy (si présents)
CHEV_TEXT_PATTERNS = [
    (r' <span class="chev">⌄</span>', CHEV_NEW),
    (r' <span class="chev">▼</span>', CHEV_NEW),
    (r' <span class="chev">▾</span>', CHEV_NEW),
]


def patch_nav_css(html: str) -> str:
    """Corrige les règles .nav existantes avant injection du bloc."""
    html = re.sub(
        r"\.nav\{display:flex;align-items:center;gap:2px;flex:1;flex-wrap:wrap;\}",
        ".nav{display:flex;align-items:center;gap:1px;flex:1;flex-wrap:nowrap;min-width:0;}",
        html,
    )
    html = re.sub(
        r"\.nav\{display:flex;align-items:center;gap:2px;flex:1;\}",
        ".nav{display:flex;align-items:center;gap:1px;flex:1;flex-wrap:nowrap;min-width:0;}",
        html,
    )
    html = re.sub(
        r"\.nav-btn \.chev\{font-size:9px;transition:transform \.2s;display:inline-block;\}",
        ".nav-btn .chev{display:inline-flex;align-items:center;transition:transform .2s;}",
        html,
    )
    html = re.sub(
        r"  \.nav\{display:flex !important;flex-wrap:wrap;gap:2px;flex:1;\}",
        "  .nav{display:flex !important;flex-wrap:nowrap !important;gap:0;flex:1;min-width:0;}",
        html,
    )
    html = re.sub(
        r"  \.nav-btn\{font-size:12px;padding:7px 10px;white-space:nowrap;\}",
        "  .nav-btn{font-size:12.5px;padding:8px 7px;white-space:nowrap;letter-spacing:-0.02em;}",
        html,
    )
    if MARKER in html:
        html = re.sub(
            r"/\* === NAVBAR LAYOUT v1[\s\S]*?\.nav-item\.open \.nav-chevron\{transform:rotate\(180deg\);\}",
            NAVBAR_CSS.strip(),
            html,
            count=1,
        )
    elif MARKER not in html:
        html = html.replace("</style>", NAVBAR_CSS + "\n</style>", 1)
    return html


def patch_nav_markup(html: str) -> str:
    if CHEV_OLD in html:
        html = html.replace(CHEV_OLD, CHEV_NEW)
    for pat, repl in CHEV_TEXT_PATTERNS:
        html = re.sub(pat, " " + repl, html)
    # nav-btn sans span.chev : ajouter chevron après le libellé (rare)
    return html


def process(html: str) -> str:
    html = patch_nav_css(html)
    html = patch_nav_markup(html)
    return html


def main():
    changed = []
    for path in sorted(ROOT.glob("*.html")):
        orig = path.read_text(encoding="utf-8")
        new = process(orig)
        if new != orig:
            path.write_text(new, encoding="utf-8")
            changed.append(path.name)
    print(f"fix_navbar_layout.py — {len(changed)} page(s) modifiée(s)")
    if changed:
        for name in changed[:5]:
            print(f"  · {name}")
        if len(changed) > 5:
            print(f"  … et {len(changed) - 5} autres")


if __name__ == "__main__":
    main()
