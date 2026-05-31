#!/usr/bin/env python3
"""Inject mobile-first hero (MOBILE HERO VD) into index + canton service pages. Idempotent."""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).parent
MARKER = "/* === MOBILE HERO VD === */"

CANTON_PREP = {
    "ge": "à Genève",
    "vd": "sur Vaud",
    "vs": "en Valais",
    "fr": "à Fribourg",
    "ne": "à Neuchâtel",
    "ju": "au Jura",
}

SERVICE_PAGES = sorted(
    p.name
    for p in BASE.glob("*-*.html")
    if re.match(r"^(ge|vd|vs|fr|ne|ju)-\w+\.html$", p.name)
)

TARGETS = ["index.html", *SERVICE_PAGES]

MOBILE_HERO_CSS = """
/* === MOBILE HERO VD === */
@media (max-width: 768px) {
  .hero {
    background: transparent;
    min-height: auto;
    color: #1f2937;
  }
  .hero::after { display: none; }
  .hero-inner {
    padding: 0;
    gap: 0;
    display: flex;
    flex-direction: column;
  }
  .hero-desktop { display: none !important; }
  .mobile-hero { display: block; }

  .mobile-hero {
    padding: 24px 16px 32px;
    background: linear-gradient(180deg, #f8faf8 0%, #ffffff 100%);
  }

  .hero-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
  }

  .badge-new {
    background: #fef3c7;
    color: #92400e;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
  }

  .badge-text {
    font-size: 12px;
    color: #6B7280;
  }

  .hero-location {
    font-size: 14px;
    color: #2E7D32;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
  }

  .hero-title {
    font-size: 28px;
    font-weight: 800;
    line-height: 1.2;
    color: #0d2818;
    margin-bottom: 12px;
  }

  .hero-accent {
    color: #2E7D32;
    display: block;
    font-size: 24px;
    margin-top: 4px;
  }

  .hero-desc {
    font-size: 15px;
    line-height: 1.6;
    color: #4B5563;
    margin-bottom: 24px;
  }

  .hero-ctas {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 24px;
  }

  .hero-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 16px;
    border-radius: 12px;
    text-decoration: none;
    font-weight: 700;
    font-size: 16px;
    position: relative;
    transition: transform 150ms ease, box-shadow 150ms ease;
  }

  .hero-btn:active { transform: scale(0.98); }

  .hero-btn--primary {
    background: #2E7D32;
    color: white;
    box-shadow: 0 4px 14px rgba(46, 125, 50, 0.3);
  }

  .hero-btn--primary svg {
    width: 28px;
    height: 28px;
    margin-bottom: 4px;
  }

  .hero-btn--secondary {
    background: white;
    color: #2E7D32;
    border: 2px solid #2E7D32;
  }

  .hero-btn--secondary svg {
    width: 22px;
    height: 22px;
    margin-bottom: 2px;
  }

  .btn-sub {
    font-size: 12px;
    font-weight: 400;
    opacity: 0.85;
  }

  .hero-trust {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  .hero-trust li {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #374151;
  }

  .hero-trust li svg {
    color: #2E7D32;
    flex-shrink: 0;
    width: 18px;
    height: 18px;
  }

  .hero-img {
    display: block !important;
    order: 2;
    height: 200px;
    margin: 0 16px 24px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  .hero-btn.phone-animate svg {
    animation: phone-ring 2.5s ease-in-out infinite;
    transform-origin: center bottom;
  }
}

@media (min-width: 769px) {
  .mobile-hero { display: none; }
}

@media (max-width: 768px) and (prefers-reduced-motion: reduce) {
  .hero-btn.phone-animate svg { animation: none !important; }
}
"""

HERO_COL_RE = re.compile(
    r"(<section class=\"hero\">\s*<div class=\"hero-inner\">\s*<div>)"
    r"(.*?)"
    r"(</div>\s*<div class=\"hero-img\">)",
    re.DOTALL,
)

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL)
HBADGE_RE = re.compile(
    r'<span class="hbadge">.*?<use href="#icon-check"/>.*?</svg>\s*([^<]+?)\s*</span>',
    re.DOTALL,
)
PREP_SPLIT_RE = re.compile(r"^(.+?)\s+((?:à|sur|en|au)\s+.+)$")


def inject_css(html: str) -> tuple[str, bool]:
    if MARKER in html:
        return html, False
    if "</style>" not in html:
        return html, False
    return html.replace("</style>", MOBILE_HERO_CSS + "\n</style>", 1), True


def split_h1(raw: str) -> tuple[str, str]:
    text = re.sub(r"<br\s*/?>", " ", raw, flags=re.I).strip()
    m = PREP_SPLIT_RE.match(text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    parts = text.split()
    if len(parts) > 2:
        return " ".join(parts[:-2]), " ".join(parts[-2:])
    return text, ""


def strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def extract_trust(content: str, defaults: list[str]) -> list[str]:
    found = [t.strip() for t in HBADGE_RE.findall(content)]
    found = [re.sub(r"\s+", " ", t) for t in found if t.strip()]
    if len(found) >= 4:
        return found[:4]
    if found:
        for extra in defaults:
            if len(found) >= 4:
                break
            if extra not in found:
                found.append(extra)
        return found[:4]
    return defaults[:4]


def fix_duplicate_trust(html: str) -> tuple[str, bool]:
    dup = (
        '<li><svg class="icon icon-sm" aria-hidden="true"><use href="#icon-check"/></svg> Sans déplacement payant</li>\n'
        "        <li><svg class=\"icon icon-sm\" aria-hidden=\"true\"><use href=\"#icon-check\"/></svg> Sans déplacement payant</li>"
    )
    fix = (
        '<li><svg class="icon icon-sm" aria-hidden="true"><use href="#icon-check"/></svg> Sans déplacement payant</li>\n'
        '        <li><svg class="icon icon-sm" aria-hidden="true"><use href="#icon-check"/></svg> Tout le canton</li>'
    )
    if dup in html:
        return html.replace(dup, fix, 1), True
    return html, False


def trust_list_html(items: list[str]) -> str:
    lines = ['      <ul class="hero-trust">']
    for label in items:
        short = label.replace(" sous 2h", "").replace(" sous 24h", "")
        lines.append(
            f'        <li><svg class="icon icon-sm" aria-hidden="true"><use href="#icon-check"/></svg> {short}</li>'
        )
    lines.append("      </ul>")
    return "\n".join(lines)


def ctas_html() -> str:
    return """      <div class="hero-ctas">
        <a href="tel:+41795805857" class="hero-btn hero-btn--primary phone-animate">
          <svg class="icon icon-btn" aria-hidden="true"><use href="#icon-phone"/></svg>
          <span>079 580 58 57</span>
          <span class="btn-sub">Appel immédiat</span>
        </a>
        <a href="#devis" class="hero-btn hero-btn--secondary">
          <svg class="icon icon-btn" aria-hidden="true"><use href="#icon-document"/></svg>
          <span>Devis gratuit</span>
          <span class="btn-sub">Réponse sous 2h</span>
        </a>
      </div>"""


def home_mobile_block() -> str:
    trust = [
        "Devis gratuit",
        "Intervention rapide",
        "6 cantons",
        "Sans déplacement payant",
    ]
    return f"""    <div class="mobile-hero">
      <div class="hero-badge">
        <span class="badge-new">NOUVEAU</span>
        <span class="badge-text">Devis gratuit sous 24h</span>
      </div>
      <p class="hero-location">Suisse romande</p>
      <h1 class="hero-title">Débarras et nettoyage<span class="hero-accent">professionnel</span></h1>
      <p class="hero-desc">Appartement, maison, succession, entrée en EMS, logement insalubre ou nettoyage extrême : <strong>Val-Débarras intervient rapidement dans toute la Suisse romande.</strong> Nous nous occupons de tout : tri, débarras, évacuation, nettoyage et remise en état.</p>
{ctas_html()}
{trust_list_html(trust)}
    </div>"""


def service_mobile_block(content: str, prep: str) -> str | None:
    h1_m = H1_RE.search(content)
    if not h1_m:
        return None
    title_main, accent = split_h1(h1_m.group(1))

    sub_m = re.search(
        r'<div class="hero-sub-title">([^<]+)</div>', content
    )
    text_m = re.search(r'<p class="hero-text">([^<]+)</p>', content)
    desc_parts = []
    if sub_m:
        desc_parts.append(sub_m.group(1).strip())
    if text_m:
        desc_parts.append(text_m.group(1).strip())
    desc = " ".join(desc_parts) if desc_parts else "Intervention rapide avec devis gratuit."

    trust_defaults = [
        "Devis gratuit",
        "Intervention rapide",
        "Tout le canton",
        "Sans déplacement payant",
    ]
    trust = extract_trust(content, trust_defaults)

    return f"""    <div class="mobile-hero">
      <div class="hero-badge">
        <span class="badge-new">NOUVEAU</span>
        <span class="badge-text">Devis gratuit sous 24h</span>
      </div>
      <p class="hero-location">{prep}</p>
      <h1 class="hero-title">{title_main}<span class="hero-accent">{accent}</span></h1>
      <p class="hero-desc">{desc}</p>
{ctas_html()}
{trust_list_html(trust)}
    </div>"""


def wrap_hero_column(html: str, filename: str) -> tuple[str, bool]:
    if 'class="mobile-hero"' in html:
        return html, False

    m = HERO_COL_RE.search(html)
    if not m:
        return html, False

    inner = m.group(2)
    if 'class="hero-desktop"' in inner:
        return html, False

    wrapped = f'{m.group(1)}\n    <div class="hero-desktop">{inner.strip()}\n    </div>\n'

    if filename == "index.html":
        mobile = home_mobile_block()
    else:
        prefix = filename.split("-")[0]
        prep = CANTON_PREP.get(prefix)
        if not prep:
            return html, False
        block = service_mobile_block(inner, prep)
        if not block:
            return html, False
        mobile = block

    new_section = wrapped + mobile + m.group(3)
    return html[: m.start()] + new_section + html[m.end() :], True


def process_file(path: Path) -> list[str]:
    changes = []
    html = path.read_text(encoding="utf-8")
    orig = html

    html, css_ok = inject_css(html)
    html, html_ok = wrap_hero_column(html, path.name)
    html, trust_ok = fix_duplicate_trust(html)

    if html != orig:
        path.write_text(html, encoding="utf-8")
        if css_ok:
            changes.append("css")
        if html_ok:
            changes.append("html")
        if trust_ok:
            changes.append("trust")
    return changes


def main() -> None:
    touched = []
    for name in TARGETS:
        path = BASE / name
        if not path.exists():
            continue
        ch = process_file(path)
        if ch:
            touched.append(f"{name} ({','.join(ch)})")

    print(f"Pages mises à jour: {len(touched)}")
    for line in touched:
        print(f"  - {line}")


if __name__ == "__main__":
    main()
