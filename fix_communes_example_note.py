#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajoute « Ceci est un exemple » avant le nuage de communes (.communes-cloud)
sur les 36 pages service (ge/vd/vs/fr/ne/ju × 6 services). Idempotent.
N'applique pas à index.html ni aux pages *-merci.html.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
CANTONS = ("ge", "vd", "vs", "fr", "ne", "ju")
SERVICES = ("appartement", "maison", "succession", "ems", "diogene", "nettoyage")
SERVICE_PAGES = [f"{c}-{s}.html" for c in CANTONS for s in SERVICES]

NOTE_HTML = '<p class="communes-example-note">Ceci est un exemple</p>'
NOTE_CSS = (
    ".communes-example-note{font-size:14px;color:#6B7280;font-style:italic;"
    "margin:0 0 12px;text-align:center;}"
)
PILL_HOVER = (
    ".commune-pill:hover{background:#009b74;color:#fff;transform:translateY(-2px);"
    "box-shadow:0 4px 12px rgba(0,155,116,.2);}"
)

HEADING_CLOUD = re.compile(
    r'(<h3>Communes couvertes[^<]+</h3>\s*)'
    r'(?!<p class="communes-example-note">)'
    r'(<div class="communes-cloud[^"]*">)'
)
# Réparation si une ancienne version du script a mangé le <div> (\2 → STX)
BROKEN_CLOUD = re.compile(
    r'(<p class="communes-example-note">Ceci est un exemple</p>\s*)\x02(\s*\n\s*<span class="commune-pill">)'
)
CLOUD_OPEN = '<div class="communes-cloud animate-on-scroll">'


def patch_html(html: str) -> tuple[str, bool]:
    changed = False
    if BROKEN_CLOUD.search(html):
        html = BROKEN_CLOUD.sub(
            r"\1" + CLOUD_OPEN + r"\2", html, count=1
        )
        changed = True

    if "communes-example-note" not in html:
        def insert_note(m: re.Match) -> str:
            return m.group(1) + NOTE_HTML + "\n    " + m.group(2)

        new_html, n = HEADING_CLOUD.subn(insert_note, html, count=1)
        if n:
            html = new_html
            changed = True

    if ".communes-example-note{" not in html and PILL_HOVER in html:
        html = html.replace(PILL_HOVER, PILL_HOVER + "\n" + NOTE_CSS, 1)
        changed = True

    return html, changed


def main():
    changed_pages = []
    for page in SERVICE_PAGES:
        path = BASE / page
        if not path.is_file():
            print("MISSING:", page)
            continue
        before = path.read_text(encoding="utf-8")
        after, ok = patch_html(before)
        if ok and after != before:
            path.write_text(after, encoding="utf-8")
            changed_pages.append(page)

    print(f"Pages modifiées: {len(changed_pages)}")
    if changed_pages:
        for p in changed_pages:
            print(" ", p)


if __name__ == "__main__":
    main()
