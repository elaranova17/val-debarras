#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_phone_animate.py — Site-wide phone icon animation + visibility on call CTAs.

Idempotent. Applies to all *.html in prototype/.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PHONE_CSS = """
/* === PHONE ANIMATE VD === */
@keyframes phone-ring{
  0%,100%{transform:rotate(0);}
  10%{transform:rotate(-12deg);}
  20%{transform:rotate(12deg);}
  30%{transform:rotate(-8deg);}
  40%{transform:rotate(8deg);}
  50%,100%{transform:rotate(0);}
}
.phone-animate > .icon-btn,
.phone-animate > .icon,
.phone-animate .icon-btn:first-child,
.phone-animate .icon:first-child{
  animation:phone-ring 2.5s ease-in-out infinite;
  transform-origin:center bottom;
}
.header-cta.phone-animate{
  background:linear-gradient(135deg,var(--vert) 0%,#1f9a6a 100%) !important;
  box-shadow:0 4px 18px rgba(0,155,116,.5),inset 0 1px 0 rgba(255,255,255,.18) !important;
  border:1px solid rgba(255,255,255,.22);
}
.header-cta.phone-animate .icon-btn{width:22px !important;height:22px !important;}
.btn-phone.phone-animate{
  box-shadow:0 4px 20px rgba(0,155,116,.35);
}
.btn-phone.phone-animate .icon-btn{width:24px !important;height:24px !important;}
.sticky-mobile__call.phone-animate,
.drawer-phone.phone-animate{
  box-shadow:0 4px 20px rgba(0,155,116,.45);
}
.sticky-mobile__call.phone-animate .icon-btn,
.drawer-phone.phone-animate .icon-btn{
  width:22px !important;height:22px !important;
}
@media (prefers-reduced-motion:reduce){
  .phone-animate > .icon-btn,
  .phone-animate > .icon,
  .phone-animate .icon-btn:first-child,
  .phone-animate .icon:first-child{animation:none !important;}
}
"""

MARKER = "PHONE ANIMATE VD"

PHONE_CLASSES = (
    "header-cta",
    "btn-phone",
    "sticky-mobile__call",
    "drawer-phone",
)

TEL_HREF = re.compile(
    r'(<a\s+href="tel:\+41795805857"\s+class=")([^"]*)(")',
    re.I,
)


def inject_css(html: str) -> str:
    if MARKER in html:
        return html
    return html.replace("</style>", PHONE_CSS + "\n</style>", 1)


def add_phone_animate_class(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        prefix, classes, suffix = m.group(1), m.group(2), m.group(3)
        if "phone-animate" in classes.split():
            return m.group(0)
        if not any(c in classes.split() for c in PHONE_CLASSES):
            # Only add to tel links that look like phone CTAs
            if not any(
                c in classes
                for c in ("header-cta", "btn-phone", "sticky-mobile__call", "drawer-phone")
            ):
                return m.group(0)
        return f'{prefix}{classes} phone-animate{suffix}'

    return TEL_HREF.sub(repl, html)


def process_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html
    html = inject_css(html)
    html = add_phone_animate_class(html)
    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.glob("*.html")):
        if process_file(path):
            changed += 1
            print(f"  ✓ {path.name}")
    print(f"fix_phone_animate.py — {changed} file(s) updated")


if __name__ == "__main__":
    main()
