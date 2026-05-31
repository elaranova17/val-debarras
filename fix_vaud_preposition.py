#!/usr/bin/env python3
"""fix_vaud_preposition.py — Idempotent fix: « dans le Vaud » → « sur Vaud ».

Swiss French convention for the canton of Vaud. Safe to re-run (no-op if already fixed).
Does not change prepositions for other cantons (à Genève, en Valais, etc.).
"""
from __future__ import annotations

import glob
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

# Longer / more specific patterns first; case-sensitive where needed.
TEXT_REPLACEMENTS: list[tuple[str, str]] = [
    ("NOTRE SERVICE DANS LE VAUD", "NOTRE SERVICE SUR VAUD"),
    ("DANS LE VAUD", "SUR VAUD"),
    ("dans tout le canton de Vaud", "sur Vaud"),
    ("dans le canton de Vaud", "sur Vaud"),
    ("dans le Canton de Vaud", "sur Vaud"),
    ("Dans le canton de Vaud", "Sur Vaud"),
    ("dans le Vaud", "sur Vaud"),
    ("Dans le Vaud", "Sur Vaud"),
]

# Python string literals in canton maps (generate_canton_pages.py, fix_links.py)
PY_REPLACEMENTS: list[tuple[str, str]] = [
    ('"prep": "dans le Vaud"', '"prep": "sur Vaud"'),
    ('"prep_in": "dans le canton de Vaud"', '"prep_in": "sur Vaud"'),
]

HTML_GLOB = os.path.join(BASE, "*.html")
PY_FILES = [
    os.path.join(BASE, "generate_canton_pages.py"),
    os.path.join(BASE, "fix_links.py"),
]


def fix_text(content: str) -> tuple[str, int]:
    """Apply Vaud preposition replacements; return (new_content, replacement_count)."""
    total = 0
    for old, new in TEXT_REPLACEMENTS:
        count = content.count(old)
        if count:
            content = content.replace(old, new)
            total += count
    return content, total


def process_file(path: str, replacements: list[tuple[str, str]] | None = None) -> int:
    with open(path, encoding="utf-8") as f:
        original = f.read()

    if replacements is not None:
        content, count = original, 0
        for old, new in replacements:
            n = content.count(old)
            if n:
                content = content.replace(old, new)
                count += n
    else:
        content, count = fix_text(original)

    if count and content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return count


def verify() -> list[str]:
    """Return list of remaining wrong patterns (empty = OK)."""
    bad: list[str] = []
    patterns = [
        r"dans le [Vv]aud",
        r"dans le [Cc]anton de [Vv]aud",
        r"dans tout le canton de Vaud",
        r"DANS LE VAUD",
    ]
    skip = {os.path.basename(__file__)}
    for path in glob.glob(HTML_GLOB) + PY_FILES:
        if not os.path.isfile(path) or os.path.basename(path) in skip:
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for pat in patterns:
            for m in re.finditer(pat, text):
                bad.append(f"{os.path.basename(path)}: {m.group()}")
    return bad


def main() -> int:
    total = 0
    files_touched: dict[str, int] = {}

    for path in sorted(glob.glob(HTML_GLOB)):
        n = process_file(path)
        if n:
            files_touched[path] = n
            total += n

    for path in PY_FILES:
        if not os.path.isfile(path):
            continue
        n = process_file(path, PY_REPLACEMENTS)
        if n:
            files_touched[path] = n
            total += n

    print(f"Replacements: {total} in {len(files_touched)} file(s)")
    for path, n in sorted(files_touched.items()):
        print(f"  {os.path.relpath(path, BASE)}: {n}")

    remaining = verify()
    if remaining:
        print("\nWARNING — remaining wrong forms:")
        for line in remaining[:20]:
            print(f"  {line}")
        if len(remaining) > 20:
            print(f"  … and {len(remaining) - 20} more")
        return 1

    print("\nVerify OK: 0 remaining « dans le Vaud » / « dans le canton de Vaud »")
    return 0


if __name__ == "__main__":
    sys.exit(main())
