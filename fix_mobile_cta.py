#!/usr/bin/env python3
"""Mobile CTA optimization — 1 bouton par viewport, sticky unique, cartes en liens.

Idempotent : relançable sur tous les *.html du prototype (sauf brand.html).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKER = "/* === MOBILE CTA OPTIMIZATION VD === */"
SKIP = {"brand.html"}

MOBILE_CTA_CSS = """
/* === MOBILE CTA OPTIMIZATION VD === */
@media (max-width: 768px) {
  /* 1 — Header : logo + hamburger uniquement */
  .header-inner {
    padding: 12px 16px !important;
    height: auto !important;
    min-height: 56px;
  }
  .header-cta,
  .header-phone,
  .header-phone-compact,
  .desktop-only-phone {
    display: none !important;
  }

  /* 2 — Hero mobile : 1 bouton devis + lien téléphone texte */
  .mobile-hero .hero-ctas {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  .mobile-hero .hero-btn--primary {
    width: 100%;
    flex-direction: row;
    gap: 10px;
    padding: 16px 20px;
    background: var(--vert, #2e7d5c);
    color: #fff;
    border: none;
    box-shadow: 0 4px 14px rgba(46, 125, 92, 0.35);
    font-size: 16px;
    font-weight: 800;
    text-align: center;
    justify-content: center;
  }
  .mobile-hero .hero-btn--primary svg {
    width: 22px;
    height: 22px;
    margin: 0;
  }
  .mobile-hero .hero-btn--secondary,
  .mobile-hero .hero-btn.phone-animate:not(.hero-btn--primary) {
    display: none !important;
  }
  .hero-phone-link-wrap {
    margin: 0;
    text-align: center;
  }
  .hero-phone-link {
    font-size: 14px;
    color: var(--gris-fonce, #1f2937);
    text-decoration: underline;
    text-underline-offset: 3px;
    font-weight: 500;
  }
  .hero-phone-link strong {
    font-weight: 700;
    color: var(--vert, #2e7d5c);
  }

  /* 3 — Étapes : pas de boutons */
  .steps-section a[class*="btn"],
  .steps-section button,
  .step a[class*="btn"],
  .step button {
    display: none !important;
  }

  /* 4 — Cartes services (accueil + autres services) */
  .sc .sc-card-primary,
  .sc .sc-cta-devis,
  .sc .btn-devis,
  .sc .btn-phone,
  .other-card .other-card-cta,
  .other-card .btn-devis,
  .other-card .btn-phone {
    display: none !important;
  }
  .sc-toggle,
  .sc-link,
  .link-details {
    display: inline-flex !important;
  }
  .other-card .link-details {
    display: block !important;
    margin-top: auto;
    font-size: 13px;
    font-weight: 700;
    color: var(--vert, #2e7d5c);
    text-decoration: underline;
    text-underline-offset: 2px;
  }

  /* Sidebar LP — pas de doublons avec sticky */
  .sidebar-cta .btn-phone,
  .sidebar-cta .btn-devis,
  .lp-sidebar .btn-phone,
  .lp-sidebar .btn-devis {
    display: none !important;
  }

  /* 5 — Footer : liens texte seulement */
  .footer .btn-phone,
  .footer-cta,
  .ft-phone-btn {
    display: none !important;
  }
  .ft-inner {
    text-align: center;
  }
  .ft-brand,
  .ft-contact {
    align-items: center;
  }
  .ft-links,
  .ft-hours {
    justify-content: center;
  }

  /* 6 — Sticky : un seul bouton devis pleine largeur */
  .sticky-mobile {
    display: flex !important;
    padding: 10px 16px calc(12px + env(safe-area-inset-bottom, 0px));
    gap: 0;
  }
  .sticky-mobile__call,
  .sticky-mobile__devis:not(.sticky-mobile__single) {
    display: none !important;
  }
  .sticky-mobile__single {
    display: flex !important;
    width: 100%;
    flex: 1 1 100%;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-height: 52px;
    padding: 14px 16px;
    border-radius: 12px;
    background: var(--vert, #2e7d5c);
    color: #fff;
    font-weight: 800;
    font-size: 15px;
    text-decoration: none;
    box-shadow: 0 4px 16px rgba(46, 125, 92, 0.35);
  }
  body.has-sticky-mobile {
    padding-bottom: calc(80px + env(safe-area-inset-bottom, 0px));
  }
}
/* === END MOBILE CTA OPTIMIZATION VD === */
"""

NEW_HERO_CTAS = """      <div class="hero-ctas">
        <a href="#devis" class="hero-btn hero-btn--primary">
          <svg class="icon icon-btn" aria-hidden="true"><use href="#icon-document"/></svg>
          <span>Devis gratuit — Réponse 24h</span>
        </a>
        <p class="hero-phone-link-wrap">
          <a href="tel:+41795805857" class="hero-phone-link">Ou appelez-nous&nbsp;: <strong>079 580 58 57</strong></a>
        </p>
      </div>"""

NEW_STICKY = """<div class="sticky-mobile" id="stickyBar">
  <a href="#devis" class="sticky-mobile__single"><svg class="icon icon-btn"><use href="#icon-document-line"/></svg>Devis gratuit — Réponse 24h</a>
</div>"""

HERO_CTAS_OLD = re.compile(
    r"<div class=\"hero-ctas\">.*?</div>\s*(?=<ul class=\"hero-trust\">|</div>\s*<div class=\"hero-img\">)",
    re.DOTALL,
)

STICKY_OLD = re.compile(
    r"<div class=\"sticky-mobile\" id=\"stickyBar\">.*?</div>",
    re.DOTALL,
)

LINK_DETAILS = '<span class="link-details">Voir le service →</span>'


def inject_css(html: str) -> tuple[str, bool]:
    if MARKER in html:
        html = re.sub(
            r"/\* === MOBILE CTA OPTIMIZATION VD === \*/[\s\S]*?"
            r"/\* === END MOBILE CTA OPTIMIZATION VD === \*/",
            MOBILE_CTA_CSS.strip(),
            html,
            count=1,
        )
        return html, True
    if "</style>" not in html:
        return html, False
    return html.replace("</style>", MOBILE_CTA_CSS + "\n</style>", 1), True


def patch_hero_ctas(html: str) -> tuple[str, bool]:
    if "hero-phone-link-wrap" in html and "Devis gratuit — Réponse 24h" in html:
        m = HERO_CTAS_OLD.search(html)
        if m and "hero-phone-link-wrap" in m.group(0):
            return html, False
    m = HERO_CTAS_OLD.search(html)
    if not m:
        return html, False
    return html[: m.start()] + NEW_HERO_CTAS + "\n" + html[m.end() :], True


def patch_sticky(html: str) -> tuple[str, bool]:
    if "sticky-mobile__single" in html:
        m = STICKY_OLD.search(html)
        if m and "sticky-mobile__single" in m.group(0):
            return html, False
    m = STICKY_OLD.search(html)
    if not m:
        return html, False
    return html[: m.start()] + NEW_STICKY + html[m.end() :], True


def patch_other_cards(html: str) -> tuple[str, bool]:
    if 'class="link-details"' in html:
        return html, False
    if 'class="other-card"' not in html:
        return html, False
    new = html.replace(
        '<span class="other-card-cta">',
        LINK_DETAILS + "\n        " + '<span class="other-card-cta" hidden>',
    )
    new = new.replace(
        '<div class="other-card-cta">',
        LINK_DETAILS + "\n        " + '<div class="other-card-cta" hidden>',
    )
    return new, new != html


def process_file(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    orig = html
    changes: list[str] = []

    html, ok = inject_css(html)
    if ok:
        changes.append("css")

    html, ok = patch_hero_ctas(html)
    if ok:
        changes.append("hero")

    html, ok = patch_sticky(html)
    if ok:
        changes.append("sticky")

    html, ok = patch_other_cards(html)
    if ok:
        changes.append("other-card")

    if html != orig:
        path.write_text(html, encoding="utf-8")
    return changes


def main() -> None:
    touched: list[str] = []
    for path in sorted(ROOT.glob("*.html")):
        if path.name in SKIP:
            continue
        ch = process_file(path)
        if ch:
            touched.append(f"{path.name} ({','.join(ch)})")

    print(f"Pages mises à jour: {len(touched)}")
    for line in touched:
        print(f"  - {line}")


if __name__ == "__main__":
    main()
