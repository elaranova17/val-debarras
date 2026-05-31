#!/usr/bin/env python3
"""
Finalisation de l'unification du design system.

Idempotent : suppression du CSS mort laissé après les swaps de markup et
standardisation du dernier lien tel: non conforme.

Ce qui a été laissé incomplet par le process précédent :
  1. `.villes-list`   -> markup déjà migré vers `.communes-cloud` (pages ge-*),
                          mais la règle CSS n'avait pas été retirée.
  2. `.photo-masonry` -> conteneur migré vers une grille inline
                          (<div style="display:grid;...">), règle CSS orpheline.
  3. `.pm-cell--tall` -> modificateur jamais utilisé dans le markup.
  4. brand.html       -> lien `tel:0795805857` non standardisé.

Re-exécutable sans effet de bord (no-op au 2e passage).
"""

import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

# Règles CSS mortes à retirer (selecteur exact, sans accolades imbriquées).
DEAD_SELECTORS = [
    r"\.villes-list",
    r"\.photo-masonry",
    r"\.pm-cell--tall",
]


def remove_dead_css(text: str) -> tuple[str, int]:
    removed = 0
    for sel in DEAD_SELECTORS:
        # Selecteur + bloc { ... } (pas d'accolade imbriquée en CSS plat ici)
        # On retire aussi l'indentation de ligne et le retour à la ligne final.
        pattern = re.compile(r"[ \t]*" + sel + r"\s*\{[^{}]*\}[ \t]*\n?")
        text, n = pattern.subn("", text)
        removed += n
    return text, removed


def standardize_tel(text: str) -> tuple[str, int]:
    # tel:0795805857  ->  tel:+41795805857  (sans toucher aux liens déjà conformes)
    pattern = re.compile(r"tel:0795805857\b")
    return pattern.subn("tel:+41795805857", text)


def main() -> None:
    total_css = 0
    total_tel = 0
    for path in sorted(ROOT.glob("*.html")):
        original = path.read_text(encoding="utf-8")
        text, css_n = remove_dead_css(original)
        text, tel_n = standardize_tel(text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"{path.name}: -{css_n} regle(s) CSS morte(s), {tel_n} tel standardise(s)")
        else:
            print(f"{path.name}: deja propre (no-op)")
        total_css += css_n
        total_tel += tel_n
    print(f"\nTotal : {total_css} regle(s) CSS retiree(s), {total_tel} lien(s) tel standardise(s).")


if __name__ == "__main__":
    main()
