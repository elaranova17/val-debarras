#!/usr/bin/env python3
"""fix_replicate_ge_design.py — Force-regenerate all canton×service pages from ge-* templates.

Uses generate_canton_pages with --force to apply the canonical Geneva design structure
(CSS, sections, other-grid, communes pills, form layout) while preserving canton-specific
content extracted from PDFs.
"""
from __future__ import annotations

import re
import sys

from generate_canton_pages import BASE, CANTONS, SERVICES, generate_page

# Clean orphaned other-grid markup left by the old non-greedy regex
OTHER_SECTION_RE = re.compile(
    r'(<section class="other-section" id="autres-services">.*?<div class="other-grid">)'
    r'(?:\s*<a\b[^>]*\bclass="other-card"[^>]*>.*?</a>\s*)*'
    r'\s*</div>'
    r'(?:\s*<h3 class="other-card-title">.*?</a>\s*</div>)?'  # orphan tail
    r'(\s*</div>\s*</section>)',
    re.S,
)


def scrub_broken_other_section(html: str) -> str:
    """Remove duplicate/orphan other-card markup from previously broken generations."""
    m = re.search(
        r'<section class="other-section" id="autres-services">(.*?)</section>',
        html,
        re.S,
    )
    if not m:
        return html
    section = m.group(0)
    cards = re.findall(r'class="other-card"', section)
    if len(cards) <= 5:
        return html
    # Keep only first other-grid block
    fixed = re.sub(
        r'(<div class="other-grid">(?:\s*<a\b[^>]*\bclass="other-card"[^>]*>.*?</a>\s*)*\s*</div>)'
        r'\s*(?:<h3 class="other-card-title">.*?</div>\s*)?',
        r'\1',
        section,
        count=1,
        flags=re.S,
    )
    return html.replace(section, fixed)


def main() -> None:
    print("=== fix_replicate_ge_design.py ===")
    updated = 0
    for service in SERVICES:
        for canton_key in CANTONS:
            if canton_key == "ge":
                continue
            path = f"{canton_key}-{service}.html"
            print(f"→ {path}")
            fname, changed = generate_page(service, canton_key, force=True)
            if changed:
                updated += 1
                print(f"  ✓ wrote {fname}")
            else:
                print(f"  ~ unchanged {fname}")

    print(f"\nDone: {updated} pages regenerated from ge-* templates")


if __name__ == "__main__":
    main()
