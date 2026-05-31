#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organise et unifie le bloc CTA foncé « Vous êtes régie / assurance / autorité ? »
(class .pro-section) présent sur les pages de service.

- Remplace l'emoji de tête du titre (🏢 👔 🤝 🏥) par l'icône line du sprite (#icon-building),
  alignée verticalement avec le texte du titre et héritant de sa couleur (blanc).
- Normalise la structure du bloc en une version canonique propre et centrée
  (carte foncée centrée, titre + paragraphe + 2 boutons canoniques centrés).
- Conserve le texte spécifique du titre et du paragraphe de chaque page (audience ciblée),
  seul l'emoji est retiré.
- Met à jour le CSS .pro-section / .pro-card / .pro-title / .pro-cta de façon cohérente.

Idempotent : relançable sans dupliquer ni casser (la forme canonique n'est pas re-matchée).
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
PAGES = [
    "index.html", "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
    "blog.html", "blog-article-1.html", "brand.html",
]

# --- CSS : ancien bloc .pro-section -> version canonique organisée ---
OLD_CSS = (
    ".pro-section{max-width:860px;margin:0 auto 64px;padding:0 24px;}\n"
    ".pro-section>div{background:var(--vert-dark);color:white;border-radius:16px;padding:36px;display:flex;flex-direction:column;gap:12px;}\n"
    ".pro-section h3{font-size:20px;font-weight:800;}\n"
    ".pro-section p{font-size:15px;color:rgba(255,255,255,.8);line-height:1.65;}"
)
NEW_CSS = (
    ".pro-section{max-width:860px;margin:0 auto 64px;padding:0 24px;}\n"
    ".pro-card{background:var(--vert-dark);color:#fff;border-radius:16px;padding:40px 36px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px;}\n"
    ".pro-title{font-size:22px;font-weight:800;line-height:1.3;display:flex;align-items:center;justify-content:center;gap:10px;margin:0;}\n"
    ".pro-title .icon{width:26px;height:26px;color:#fff;flex-shrink:0;}\n"
    ".pro-card p{font-size:15px;color:rgba(255,255,255,.82);line-height:1.65;max-width:620px;margin:0;}"
)

OLD_CTA = ".pro-cta{margin-top:6px;}"
NEW_CTA = ".pro-cta{margin-top:8px;justify-content:center;gap:12px;}"

# --- Markup : bloc original -> bloc canonique ---
BLOCK_RE = re.compile(
    r"<section class='pro-section'><div><div class=\"pro-section\">"
    r"<h3>(?P<h>[^<]*)</h3><p>(?P<p>[^<]*)</p>.*?</section>",
    re.DOTALL,
)

LEADING_EMOJI_RE = re.compile(r"^[^0-9A-Za-zÀ-ÿ]+")


def build_block(heading, paragraph):
    heading = LEADING_EMOJI_RE.sub("", heading.strip()).strip()
    paragraph = paragraph.strip()
    return (
        '<section class="pro-section"><div class="pro-card">'
        '<h3 class="pro-title"><svg class="icon" aria-hidden="true"><use href="#icon-building"/></svg>'
        f'<span>{heading}</span></h3>'
        f'<p>{paragraph}</p>'
        '<div class="hero-btns pro-cta">'
        '<a href="tel:+41795805857" class="btn-phone">'
        '<svg class="icon icon-btn"><use href="#icon-phone-line"/></svg>079 580 58 57</a> '
        '<a href="#devis" class="btn-devis">'
        '<svg class="icon icon-btn"><use href="#icon-document-line"/></svg>Devis gratuit</a>'
        '</div></div></section>'
    )


def main():
    changed = []
    for page in PAGES:
        p = BASE / page
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        before = html

        html = html.replace(OLD_CSS, NEW_CSS)
        html = html.replace(OLD_CTA, NEW_CTA)
        html = BLOCK_RE.sub(
            lambda m: build_block(m.group("h"), m.group("p")), html
        )

        if html != before:
            p.write_text(html, encoding="utf-8")
            changed.append(page)

    print("Pages modifiées :", ", ".join(changed) if changed else "aucune")


if __name__ == "__main__":
    main()
