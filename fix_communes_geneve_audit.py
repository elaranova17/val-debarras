#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aligne les listes de communes genevoises sur les PDF source (Textos base ADS).

Les PDF définissent des listes différentes par service — on ne les unifie PAS.
On corrige seulement les écarts évidents vs PDF :
  - ge-appartement : +Cologny, +Versoix, -Satigny (Debarras_appartement_Geneve.pdf)
  - ge-succession  : retire Bernex, Cologny, Plan-les-Ouates (Debarras_Succession_Geneve.pdf)
  - ge-nettoyage   : liste complète PDF (Nettoyage Extreme Geneve Page Complete Seo Google Ads.pdf)
  - ge-ems, ge-diogene, ge-maison : inchangés (conformes ou PDF sans liste complète)

Idempotent.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent

# Listes canoniques extraites des PDF
COMMUNES = {
    "ge-appartement.html": [
        "Genève", "Carouge", "Meyrin", "Vernier", "Lancy", "Onex", "Thônex", "Bernex",
        "Grand-Saconnex", "Chêne-Bougeries", "Cologny", "Plan-les-Ouates", "Versoix",
    ],
    "ge-succession.html": [
        "Genève", "Carouge", "Lancy", "Meyrin", "Vernier", "Onex", "Thônex",
        "Grand-Saconnex", "Chêne-Bougeries",
    ],
    "ge-nettoyage.html": [
        "Genève", "Carouge", "Meyrin", "Vernier", "Lancy", "Onex", "Plan-les-Ouates",
        "Thônex", "Versoix", "Grand-Saconnex", "Chêne-Bourg", "Chêne-Bougeries", "Satigny",
        "Veyrier", "Bernex", "Confignon", "Pregny-Chambésy", "Cologny",
        "… et toutes les communes du canton",
    ],
}

CLOUD_PAT = re.compile(r'(<div class="communes-cloud">)(.*?)(</div>)', re.DOTALL)


def pills_html(communes):
    lines = [f'      <span class="commune-pill">{c}</span>' for c in communes]
    return "\n".join(lines)


def set_communes(html, communes):
    m = CLOUD_PAT.search(html)
    if not m:
        return html, False
    new_cloud = m.group(1) + "\n" + pills_html(communes) + "\n    " + m.group(3)
    return html[: m.start()] + new_cloud + html[m.end() :], True


def main():
    changed = []
    for page, communes in COMMUNES.items():
        path = BASE / page
        html = path.read_text(encoding="utf-8")
        before = html
        html, ok = set_communes(html, communes)
        if ok and html != before:
            path.write_text(html, encoding="utf-8")
            changed.append(page)
    print("Pages modifiées:", ", ".join(changed) if changed else "aucune")


if __name__ == "__main__":
    main()
