#!/usr/bin/env python3
"""fix_links.py — Fix autres-services grid links to match page canton (scoped)."""
from __future__ import annotations

import glob
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

CANTONS = {
    "ge": {"slug": "geneve", "prep": "à Genève"},
    "vd": {"slug": "vaud", "prep": "sur Vaud"},
    "vs": {"slug": "valais", "prep": "en Valais"},
    "fr": {"slug": "fribourg", "prep": "à Fribourg"},
    "ne": {"slug": "neuchatel", "prep": "à Neuchâtel"},
    "ju": {"slug": "jura", "prep": "au Jura"},
}

SERVICE_PATHS = [
    "debarras-maison",
    "debarras-apres-deces",
    "debarras-ems",
    "debarras-insalubre-diogene",
    "nettoyage-extreme",
]


def page_info(filename: str) -> tuple[str, str] | None:
    m = re.match(
        r"^(ge|vd|vs|fr|ne|ju)-(appartement|maison|succession|ems|diogene|nettoyage)\.html$",
        filename,
    )
    return (m.group(1), m.group(2)) if m else None


def fix_other_grid(html: str, canton_key: str) -> tuple[str, int]:
    """Only rewrite hrefs inside .other-grid — never touch nav/footer."""
    slug = CANTONS[canton_key]["slug"]
    prep = CANTONS[canton_key]["prep"]
    fixes = 0

    m = re.search(r'(<div class="other-grid">)(.*?)(</div>)', html, re.S)
    if not m:
        return html, 0

    grid = m.group(2)
    for path in SERVICE_PATHS:
        for ck, cv in CANTONS.items():
            wrong = f"/{path}/{cv['slug']}/"
            correct = f"/{path}/{slug}/"
            if wrong != correct and wrong in grid:
                grid = grid.replace(wrong, correct)
                fixes += 1

    new_heading = f'<h2>Autres services {prep}</h2>'
    html = re.sub(r"<h2>Autres services [^<]+</h2>", new_heading, html, count=1)
    new_html = html[: m.start(2)] + grid + html[m.end(2) :]
    return new_html, fixes


def main():
    print("=== fix_links.py ===")
    total = 0
    for path in sorted(glob.glob(os.path.join(BASE, "*-*.html"))):
        fname = os.path.basename(path)
        info = page_info(fname)
        if not info:
            continue
        canton_key, _ = info
        with open(path, encoding="utf-8") as f:
            html = f.read()
        new_html, fixes = fix_other_grid(html, canton_key)
        total += fixes
        if new_html != html:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_html)
            print(f"  ✓ {fname}: {fixes} autres-services fixes")
        else:
            print(f"  ~ {fname}")
    print(f"\nTotal fixes: {total}")


if __name__ == "__main__":
    main()
