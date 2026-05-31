#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formulaire unique: le form-card des 6 pages de service devient identique
à celui de la home (canonique). On conserve uniquement la pré-sélection
du service + canton par page (même formulaire, juste pré-rempli).
Ajoute aussi le smooth-scroll vers #devis. Idempotent.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent

# Service pré-sélectionné par page (texte d'option = celui de la home)
SERVICE_BY_PAGE = {
    "ge-appartement.html": "Débarras appartement",
    "ge-maison.html": "Débarras maison",
    "ge-succession.html": "Débarras après décès/succession",
    "ge-ems.html": "Débarras suite entrée EMS",
    "ge-diogene.html": "Débarras Insalubre/Diogène",
    "ge-nettoyage.html": "Nettoyages extrême",
}

ALL_PAGES = list(SERVICE_BY_PAGE) + ["index.html", "blog.html", "blog-article-1.html"]

FORM_CARD_RE = re.compile(
    r'<div class="form-card">\s*<form>.*?</form>\s*</div>', re.DOTALL
)


def extract_canonical():
    home = (BASE / "index.html").read_text(encoding="utf-8")
    m = FORM_CARD_RE.search(home)
    if not m:
        raise SystemExit("No se encontró el form-card canónico en index.html")
    return m.group(0)


def preselect(form_card, service):
    """Pré-sélectionne le service de la page et le canton Genève."""
    fc = form_card
    # Service
    fc = fc.replace(
        '<option value="" disabled selected>Choisir un service</option>',
        '<option value="" disabled>Choisir un service</option>', 1)
    fc = fc.replace(f'<option>{service}</option>',
                    f'<option selected>{service}</option>', 1)
    # Canton -> Genève (pages ge-*)
    fc = fc.replace(
        '<option value="" disabled selected>Choisir un canton</option>',
        '<option value="" disabled>Choisir un canton</option>', 1)
    fc = fc.replace('<option>Genève</option>',
                    '<option selected>Genève</option>', 1)
    return fc


def main():
    canonical = extract_canonical()
    changed = []

    for page, service in SERVICE_BY_PAGE.items():
        p = BASE / page
        html = p.read_text(encoding="utf-8")
        before = html
        new_fc = preselect(canonical, service)
        html, n = FORM_CARD_RE.subn(lambda _m: new_fc, html, count=1)
        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(f"{page} (form unifié, {service} présélectionné)")

    # Smooth scroll vers #devis sur toutes les pages
    for page in ALL_PAGES:
        p = BASE / page
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        if 'scroll-behavior:smooth' not in html and 'scroll-behavior: smooth' not in html:
            html = html.replace('</style>', 'html{scroll-behavior:smooth;}</style>', 1)
            p.write_text(html, encoding="utf-8")
            changed.append(f"{page} (smooth-scroll)")

    print("Cambios:")
    for c in changed:
        print("  -", c)
    if not changed:
        print("  (ninguno)")


if __name__ == "__main__":
    main()
