#!/usr/bin/env python3
"""Inject mobile zones + form CSS fixes. Idempotent."""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).parent
HTML_FILES = sorted(BASE.glob("*.html"))
MARKER = "/* === MOBILE ZONES + FORM VD === */"
END = "/* === END MOBILE ZONES + FORM VD === */"

MOBILE_ZONES_FORM_CSS = f"""{MARKER}
@media (max-width: 768px) {{
  /* Formulaire — une colonne (override PATCH form desktop) */
  .form-inner{{
    grid-template-columns:1fr !important;
    gap:32px !important;
  }}
  .form-card{{order:-1 !important;}}
  .form-section{{padding:56px 0 calc(72px + env(safe-area-inset-bottom,0px));}}
  .form-card{{padding:24px 16px !important;}}
  .fl input,.fl select,.fl textarea{{
    min-height:52px !important;
    font-size:16px !important;
  }}
  .form-btn{{
    width:100% !important;
    min-height:52px !important;
    justify-content:center;
  }}

  /* Zones d'intervention — cartes services (accueil) */
  .sc-zones{{margin-top:16px;padding-top:14px;}}
  .sc-zones-label{{font-size:11px;margin-bottom:10px;}}
  .sc-zones-links{{
    grid-template-columns:repeat(2,1fr) !important;
    gap:8px !important;
  }}
  .sc-zones-links a{{
    min-height:44px !important;
    font-size:13px !important;
    padding:8px 6px !important;
  }}

  /* Communes couvertes — pages service */
  .communes-cloud{{
    display:flex;flex-wrap:wrap;gap:8px;
    justify-content:center;padding:0 4px;
  }}
  .commune-pill{{
    min-height:44px !important;
    padding:10px 14px !important;
    font-size:13px !important;
  }}

  /* Grille cantons accueil */
  .canton-grid,.cpill-row{{
    grid-template-columns:repeat(2,1fr) !important;
    gap:10px !important;
  }}
  .canton-btn,.cpill{{
    min-height:48px !important;
    font-size:13px !important;
  }}
}}
{END}
"""

BLOCK_RE = re.compile(re.escape(MARKER) + r"[\s\S]*?" + re.escape(END), re.I)


def inject_css(html: str) -> tuple[str, bool]:
    block = MOBILE_ZONES_FORM_CSS.strip()
    if MARKER in html:
        m = BLOCK_RE.search(html)
        if m and m.group(0).strip() == block:
            return html, False
        return BLOCK_RE.sub(block, html, count=1), True
    if "</style>" not in html:
        return html, False
    return html.replace("</style>", block + "\n</style>", 1), True


def main() -> None:
    touched = []
    for path in HTML_FILES:
        html = path.read_text(encoding="utf-8")
        new, ok = inject_css(html)
        if ok:
            path.write_text(new, encoding="utf-8")
            touched.append(path.name)
    print(f"Pages mises à jour: {len(touched)}")
    for name in touched:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
