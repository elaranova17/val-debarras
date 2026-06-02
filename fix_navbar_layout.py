#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Navbar desktop — menu centré logo/CTA (≥1025px) + chevrons dropdown visibles.

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
  .header-inner{
    display:grid;
    grid-template-columns:auto 1fr auto;
    align-items:center;
    gap:6px;
    padding:0 12px;
  }
  .logo{margin-right:0;gap:0;flex-shrink:0;grid-column:1;}
  .logo-top{align-items:flex-end;}
  .logo-sub{margin-top:-4px;}
  .logo-img{width:48px;}
  .logo-name{font-size:16px !important;}
  .logo-sub{font-size:10px !important;}
  .nav{
    grid-column:2;
    flex:1 1 auto;min-width:0;
    flex-wrap:nowrap !important;
    justify-content:center !important;
    gap:2px;
  }
  .nav-btn{
    font-size:13px;
    font-weight:600;
    color:#374151;
    padding:7px 6px;
    gap:6px;
    letter-spacing:normal;
    white-space:nowrap;
  }
  .header-cta{
    grid-column:3;
    font-size:12px !important;
    padding:7px 10px !important;
    min-height:auto !important;
    gap:4px !important;
    flex-shrink:0;
  }
  .header-cta .icon-btn{width:16px !important;height:16px !important;}
}
@media(min-width:1025px) and (max-width:1279px){
  .header-inner{gap:4px;padding:0 10px;}
  .logo-img{width:44px;}
  .logo-name{font-size:15px !important;}
  .nav{gap:1px;}
  .nav-btn{
    font-size:13px;
    padding:7px 5px;
    gap:6px;
  }
  .header-cta{
    font-size:11.5px !important;
    padding:6px 9px !important;
  }
}
.nav-btn .chev{
  font-size:inherit;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  line-height:1;
  padding:2px;
  border-radius:4px;
  background:rgba(0,155,116,.12);
  transition:transform .2s,background .2s;
}
.nav-btn .nav-chevron,
.nav-btn .nav-chevron.icon-sm{
  width:18px !important;
  height:18px !important;
  opacity:1 !important;
  color:#047857 !important;
  flex-shrink:0;
  transition:transform .2s,color .2s;
}
.nav-item:hover .nav-chevron{color:#065f46 !important;}
.nav-item:hover .chev{background:rgba(0,155,116,.2);}
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
        "  .nav-btn{font-size:13px;padding:7px 6px;white-space:nowrap;letter-spacing:normal;font-weight:600;color:#374151;gap:6px;}",
        html,
    )
    html = re.sub(
        r"  \.nav-btn\{font-size:12\.5px;padding:8px 7px;white-space:nowrap;letter-spacing:-0\.02em;\}",
        "  .nav-btn{font-size:13px;padding:7px 6px;white-space:nowrap;letter-spacing:normal;font-weight:600;color:#374151;gap:6px;}",
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
