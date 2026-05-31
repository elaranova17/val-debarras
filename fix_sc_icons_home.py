#!/usr/bin/env python3
"""fix_sc_icons_home.py — Improve service card icon visibility on index.html."""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE, "index.html")

ICON_PATCH = """
/* === SERVICE CARD ICONS — visibilité accrue (home) === */
.sc-icon{
  position:absolute;top:22px;right:22px;
  opacity:1 !important;
  width:56px;height:56px;
  display:flex;align-items:center;justify-content:center;
  background:rgba(255,255,255,.12);
  border:1.5px solid rgba(255,255,255,.22);
  border-radius:14px;
  padding:8px;
  box-shadow:0 4px 14px rgba(0,0,0,.15);
}
.sc-icon .icon{
  width:48px !important;height:48px !important;
  color:#6ee7a0 !important;
  stroke-width:2;
  filter:drop-shadow(0 1px 2px rgba(0,0,0,.25));
}
.sc-icon .icon-orange{color:#fbbf24 !important;}
.sc:hover .sc-icon{
  background:rgba(255,255,255,.18);
  border-color:rgba(255,255,255,.35);
  transform:scale(1.06);
}
"""

ICON_SYSTEM_UPDATE = (
    ".sc-icon .icon{width:40px;height:40px;color:#009b74;}"
    ".sc-icon .icon{width:48px;height:48px;color:#6ee7a0;}"
)


def main():
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()
    original = html

    # Remove old faint opacity rule
    html = re.sub(
        r"\.sc-icon\{position:absolute;top:28px;right:28px;font-size:32px;opacity:\.15;\}",
        "",
        html,
    )

    if "SERVICE CARD ICONS — visibilité accrue" not in html:
        html = html.replace("</style>", ICON_PATCH + "\n</style>", 1)

    html = html.replace(ICON_SYSTEM_UPDATE.split("→")[0] if "→" in ICON_SYSTEM_UPDATE else ".sc-icon .icon{width:40px;height:40px;color:#009b74;}", ".sc-icon .icon{width:48px;height:48px;color:#6ee7a0;}")

    # Add En savoir plus links on service cards → Geneva default pages
    service_links = {
        "Débarras appartement": "/debarras-appartement/geneve/",
        "Débarras maison": "/debarras-maison/geneve/",
        "Débarras après décès & succession": "/debarras-apres-deces/geneve/",
        "Débarras suite entrée en EMS": "/debarras-ems/geneve/",
        "Débarras insalubre / Diogène": "/debarras-insalubre-diogene/geneve/",
        "Nettoyages extrême": "/nettoyage-extreme/geneve/",
    }
    for svc, href in service_links.items():
        # Add sc-link after sc-toggle if missing
        pattern = rf'(<div class="sc" data-service="{re.escape(svc)}">.*?<button class="sc-toggle"[^>]*>.*?</button>)'
        if re.search(pattern, html, re.S) and f'data-service="{svc}"' in html:
            link_html = f'\n        <a href="{href}" class="sc-link">En savoir plus →</a>'
            if link_html.strip() not in html:
                html = re.sub(
                    rf'(<div class="sc" data-service="{re.escape(svc)}">.*?<button class="sc-toggle"[^>]*>.*?</button>)',
                    rf"\1{link_html}",
                    html,
                    count=1,
                    flags=re.S,
                )

    if html != original:
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(html)
        print("✓ fix_sc_icons_home.py — index.html updated")
    else:
        print("~ fix_sc_icons_home.py — no changes")


if __name__ == "__main__":
    main()
