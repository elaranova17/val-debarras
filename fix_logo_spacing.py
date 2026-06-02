#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resserre l'espacement typographique entre le nom « Val-Débarras » et le slogan
dans tous les blocs logo (header, footer, variantes legacy), sans déplacer le layout global.

Idempotent : relançable sans effet de bord.
Cible tous les *.html du dossier prototype.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKER_START = "/* === LOGO SPACING VD === */"
MARKER_END = "/* === END LOGO SPACING VD */"

LOGO_SPACING_CSS = """
/* === LOGO SPACING VD === */
/* Header — structure logo-top + logo-sub (actuelle) */
.logo{gap:1px !important;}
.logo-top{align-items:flex-end;}
.logo-text{
  display:flex !important;
  flex-direction:column;
  gap:0 !important;
  line-height:1.1 !important;
}
.logo-name,
.footer__logo-brand,
.ft-logo-name{
  margin-bottom:2px !important;
  padding-bottom:0 !important;
  line-height:1.1 !important;
}
.logo-sub,
.footer__logo-suffix,
.ft-tagline{
  margin-top:0 !important;
  padding-top:0 !important;
  line-height:1.2 !important;
}
.logo-sub{margin-top:-2px !important;}
@media(max-width:768px){
  .header .logo-name{
    margin-bottom:1px !important;
    line-height:1.05 !important;
  }
  .header .logo-sub{
    margin-top:-3px !important;
    line-height:1.15 !important;
  }
}
.ft-brand .ft-logo-name{margin-bottom:2px !important;}
.ft-brand .ft-tagline{
  margin-top:-2px !important;
  line-height:1.2 !important;
}
@media(min-width:1025px){
  .logo{gap:0 !important;}
  .logo-top{align-items:flex-end;}
  .logo-sub{margin-top:-4px !important;}
}
/* === END LOGO SPACING VD === */
"""

BLOCK_RE = re.compile(
    r"/\* === LOGO SPACING VD === \*/[\s\S]*?/\* === END LOGO SPACING VD === \*/"
)


def inject_before_navbar(html: str) -> str:
    """Insère le bloc avant NAVBAR LAYOUT s'il existe, sinon avant </style>."""
    if "NAVBAR LAYOUT v1" in html:
        return html.replace(
            "/* === NAVBAR LAYOUT v1",
            LOGO_SPACING_CSS.strip() + "\n\n\n/* === NAVBAR LAYOUT v1",
            1,
        )
    return html.replace("</style>", LOGO_SPACING_CSS + "\n</style>", 1)


def process(html: str) -> str:
    if MARKER_START in html:
        return BLOCK_RE.sub(LOGO_SPACING_CSS.strip(), html, count=1)
    return inject_before_navbar(html)


def main():
    changed = []
    for path in sorted(ROOT.glob("*.html")):
        orig = path.read_text(encoding="utf-8")
        new = process(orig)
        if new != orig:
            path.write_text(new, encoding="utf-8")
            changed.append(path.name)
    print(f"fix_logo_spacing.py — {len(changed)} page(s) modifiée(s)")
    for name in changed[:8]:
        print(f"  · {name}")
    if len(changed) > 8:
        print(f"  … et {len(changed) - 8} autres")


if __name__ == "__main__":
    main()
