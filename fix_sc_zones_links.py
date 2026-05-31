#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_sc_zones_links.py — Home service cards: centered icons + canton zone links.

Idempotent. Updates index.html only (service cards grid).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

CANTONS = [
    ("geneve", "à Genève"),
    ("vaud", "sur Vaud"),
    ("valais", "en Valais"),
    ("fribourg", "à Fribourg"),
    ("neuchatel", "à Neuchâtel"),
    ("jura", "au Jura"),
]

SERVICES = [
    ("Débarras appartement", "debarras-appartement"),
    ("Débarras maison", "debarras-maison"),
    ("Débarras après décès & succession", "debarras-apres-deces"),
    ("Débarras suite entrée en EMS", "debarras-ems"),
    ("Débarras insalubre / Diogène", "debarras-insalubre-diogene"),
    ("Nettoyages extrême", "nettoyage-extreme"),
]

SC_ZONES_CSS = """
/* === SERVICE CARD ZONES + centered icons (home) === */
.sc-num{
  position:absolute;top:22px;left:22px;
  margin-bottom:0;
}
.sc-head{
  display:flex;flex-direction:column;align-items:center;
  text-align:center;margin-bottom:6px;
}
.sc-icon{
  position:relative !important;top:auto !important;right:auto !important;
  margin:0 auto 14px;
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
}
.sc-head .sc-title{margin-bottom:0;text-align:center;}

.sc-zones{
  margin-top:14px;padding-top:12px;
  border-top:1px solid rgba(255,255,255,.1);
}
.sc-zones-label{
  display:block;font-size:10px;font-weight:700;
  text-transform:uppercase;letter-spacing:.6px;
  color:rgba(255,255,255,.45);margin-bottom:8px;
}
.sc-zones-links{
  display:flex;flex-wrap:wrap;gap:6px 8px;
}
.sc-zones-links a{
  font-size:11.5px;font-weight:600;
  color:rgba(255,255,255,.72);
  padding:4px 10px;border-radius:20px;
  background:rgba(255,255,255,.08);
  border:1px solid rgba(255,255,255,.15);
  transition:color .2s,background .2s,border-color .2s,transform .2s;
  text-decoration:none;
}
.sc-zones-links a:hover{
  color:white;
  background:rgba(255,255,255,.18);
  border-color:rgba(255,255,255,.32);
  transform:translateY(-1px);
}
@media(max-width:768px){
  .sc-zones-links{gap:5px 6px;}
  .sc-zones-links a{font-size:11px;padding:3px 8px;}
}
"""

MARKER = "SERVICE CARD ZONES + centered icons"


def zones_html(service_slug: str) -> str:
    links = "\n".join(
        f'          <a href="/{service_slug}/{canton}/">{label}</a>'
        for canton, label in CANTONS
    )
    return f"""        <div class="sc-zones">
          <span class="sc-zones-label">Zones d'intervention :</span>
          <div class="sc-zones-links">
{links}
          </div>
        </div>"""


def inject_css(html: str) -> str:
    # Remove legacy top-right icon block if present
    html = re.sub(
        r"/\* === SERVICE CARD ICONS — visibilité accrue \(home\) === \*/\s*"
        r"\.sc-icon\{[^}]+\}\s*"
        r"\.sc-icon \.icon\{[^}]+\}\s*"
        r"\.sc-icon \.icon-orange\{[^}]+\}\s*"
        r"\.sc:hover \.sc-icon\{[^}]+\}\s*",
        "",
        html,
        flags=re.S,
    )
    if MARKER in html:
        return html
    return html.replace("</style>", SC_ZONES_CSS + "\n</style>", 1)


def restructure_card(html: str, service_name: str, service_slug: str) -> str:
    zones = zones_html(service_slug)
    # Replace old link-secondary zone link
    old_link_pat = (
        rf'(<div class="sc" data-service="{re.escape(service_name)}">.*?'
        rf'<a href="#devis" class="btn-primary sc-card-primary"[^>]*>.*?</a>\s*)'
        rf'<a href="[^"]*" class="link-secondary sc-link">Voir les zones d\'intervention →</a>'
    )
    if re.search(old_link_pat, html, re.S):
        html = re.sub(
            old_link_pat,
            rf"\1{zones}",
            html,
            count=1,
            flags=re.S,
        )
    elif f'class="sc-zones"' not in html.split(f'data-service="{service_name}"')[1].split("</div>")[0]:
        # Insert zones after primary CTA if link already replaced
        pat = (
            rf'(<div class="sc" data-service="{re.escape(service_name)}">.*?'
            rf'(<a href="#devis" class="btn-primary sc-card-primary"[^>]*>.*?</a>)\s*)'
            rf'(?!\s*<div class="sc-zones">)'
        )
        html = re.sub(pat, rf"\1{zones}\n        ", html, count=1, flags=re.S)

    # Restructure icon + title into sc-head (idempotent)
    head_pat = (
        rf'(<div class="sc" data-service="{re.escape(service_name)}">\s*)'
        rf'<span class="sc-icon">(.*?)</span>\s*'
        rf'<span class="sc-num">(\d+)</span>\s*'
        rf'<div>\s*'
        rf'<div class="sc-title">(.*?)</div>\s*'
        rf'<p class="sc-desc">(.*?)</p>\s*'
        rf'</div>'
    )
    if re.search(head_pat, html, re.S):
        html = re.sub(
            head_pat,
            rf'\1<span class="sc-num">\3</span>\n        <div class="sc-head">\n'
            rf'          <span class="sc-icon">\2</span>\n'
            rf'          <div class="sc-title">\4</div>\n'
            rf'        </div>\n'
            rf'        <p class="sc-desc">\5</p>',
            html,
            count=1,
            flags=re.S,
        )
    return html


def main() -> None:
    if not INDEX.exists():
        print("✗ index.html not found")
        return
    html = INDEX.read_text(encoding="utf-8")
    original = html
    html = inject_css(html)
    for name, slug in SERVICES:
        html = restructure_card(html, name, slug)
    if html != original:
        INDEX.write_text(html, encoding="utf-8")
        print("✓ fix_sc_zones_links.py — index.html updated")
    else:
        print("~ fix_sc_zones_links.py — no changes")


if __name__ == "__main__":
    main()
