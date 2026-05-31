#!/usr/bin/env python3
"""generate_canton_pages.py — Idempotent bulk generation of canton×service pages.

Clones ge-* templates, applies PDF content from Textos base ADS/, fixes canton-specific
links (autres services, breadcrumb, form, communes, sidebar).
"""
from __future__ import annotations

import glob
import os
import re
import subprocess
import json

BASE = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(os.path.dirname(BASE), "Textos base ADS")

CANTONS = {
    "ge": {
        "name": "Genève",
        "prep": "à Genève",
        "prep_in": "à Genève",
        "slug": "geneve",
        "pdf": "Geneve",
    },
    "vd": {
        "name": "Vaud",
        "prep": "dans le Vaud",
        "prep_in": "dans le canton de Vaud",
        "slug": "vaud",
        "pdf": "Vaud",
    },
    "vs": {
        "name": "Valais",
        "prep": "en Valais",
        "prep_in": "en Valais",
        "slug": "valais",
        "pdf": "Valais",
    },
    "fr": {
        "name": "Fribourg",
        "prep": "à Fribourg",
        "prep_in": "à Fribourg",
        "slug": "fribourg",
        "pdf": "Fribourg",
    },
    "ne": {
        "name": "Neuchâtel",
        "prep": "à Neuchâtel",
        "prep_in": "à Neuchâtel",
        "slug": "neuchatel",
        "pdf": "Neuchatel",
    },
    "ju": {
        "name": "Jura",
        "prep": "au Jura",
        "prep_in": "au Jura",
        "slug": "jura",
        "pdf": "Jura",
    },
}

SERVICES = {
    "appartement": {
        "template": "ge-appartement.html",
        "url_path": "debarras-appartement",
        "breadcrumb": "Débarras appartement",
        "form_option": "Débarras appartement",
        "h1_service": "Débarras appartement",
        "section_h2_tpl": "Débarras d'appartement {prep} — Intervention rapide",
        "hero_sub_tpl": "Intervention rapide dans tout le canton · Aucun tri demandé",
        "communes_heading_tpl": "Communes couvertes {prep}",
        "pdf_globs": ["Debarras_appartement_{pdf}.pdf"],
    },
    "maison": {
        "template": "ge-maison.html",
        "url_path": "debarras-maison",
        "breadcrumb": "Débarras maison",
        "form_option": "Débarras maison",
        "h1_service": "Débarras maison",
        "section_h2_tpl": "Débarras de maison {prep} — Intervention rapide",
        "hero_sub_tpl": "Villas, maisons familiales et propriétés · Tout le canton",
        "communes_heading_tpl": "Communes couvertes {prep}",
        "pdf_globs": [
            "Debarras_Maison_{pdf}.pdf",
            "Debarras_Maison_{pdf}_Val_Debarras.pdf",
            "Debarras_Maison_{pdf}_Val_Debarras (1).pdf",
            "Debarras_Maison_{pdf}_Val_Debarras (2).pdf",
            "Debarras_maison_{pdf}_luxe.pdf",
            "Debarras_maison_{pdf}_luxe (1).pdf",
        ],
    },
    "succession": {
        "template": "ge-succession.html",
        "url_path": "debarras-apres-deces",
        "breadcrumb": "Débarras après décès",
        "form_option": "Débarras après décès/succession",
        "h1_service": "Débarras après décès",
        "section_h2_tpl": "Débarras après décès {prep} — Accompagnement humain",
        "hero_sub_tpl": "Discrétion et respect · Accompagnement des familles",
        "communes_heading_tpl": "Communes couvertes {prep}",
        "pdf_globs": ["Debarras_Succession_{pdf}.pdf"],
    },
    "ems": {
        "template": "ge-ems.html",
        "url_path": "debarras-ems",
        "breadcrumb": "Débarras suite entrée EMS",
        "form_option": "Débarras suite entrée EMS",
        "h1_service": "Débarras EMS",
        "section_h2_tpl": "Débarras suite entrée EMS {prep}",
        "hero_sub_tpl": "Libération rapide du logement · Respect du rythme familial",
        "communes_heading_tpl": "Communes couvertes {prep}",
        "pdf_globs": ["Debarras_EMS_{pdf}.pdf", "Debarras_EMS_{pdf} (1).pdf"],
    },
    "diogene": {
        "template": "ge-diogene.html",
        "url_path": "debarras-insalubre-diogene",
        "breadcrumb": "Débarras Insalubre/Diogène",
        "form_option": "Débarras Insalubre/Diogène",
        "h1_service": "Nettoyage Diogène",
        "section_h2_tpl": "Nettoyage insalubre / Diogène {prep}",
        "hero_sub_tpl": "Sans jugement · Intervention discrète et professionnelle",
        "communes_heading_tpl": "Communes couvertes {prep}",
        "pdf_globs": ["FINAL_Diogene_{pdf}_Complet.pdf", "FINAL_Diogene_{pdf}_Complet (1).pdf"],
    },
    "nettoyage": {
        "template": "ge-nettoyage.html",
        "url_path": "nettoyage-extreme",
        "breadcrumb": "Nettoyages extrême",
        "form_option": "Nettoyages extrême",
        "h1_service": "Nettoyage extrême",
        "section_h2_tpl": "Nettoyage extrême {prep}",
        "hero_sub_tpl": "Intervention discrète 24h–48h · Décontamination professionnelle",
        "communes_heading_tpl": "Communes couvertes {prep}",
        "pdf_globs": [
            "Nettoyage_Extreme_{pdf}_9_Pages_Complet.pdf",
            "Nettoyage Extreme {pdf} Page Complete Seo Google Ads.pdf",
        ],
    },
}

ALL_OTHER_SERVICES = [
    ("appartement", "debarras-appartement", "Débarras appartement", "Studio, loft, immeuble", "icon-building"),
    ("maison", "debarras-maison", "Débarras maison", "Maison, garage, cave", "icon-house"),
    ("succession", "debarras-apres-deces", "Débarras après décès/succession", "Avec respect et discrétion", "icon-dove"),
    ("ems", "debarras-ems", "Débarras suite entrée EMS", "Libération rapide", "icon-hospital"),
    ("diogene", "debarras-insalubre-diogene", "Débarras Insalubre/Diogène", "Sans jugement", "icon-warning", True),
    ("nettoyage", "nettoyage-extreme", "Nettoyages extrême", "Désinfection professionnelle", "icon-broom"),
]

HERO_IMAGES = {
    "ge": "ge-hero.jpg",
    "vd": "vd-hero.jpg",
    "vs": "vs-hero.jpg",
    "fr": "fr-hero.jpg",
    "ne": "ne-hero.jpg",
    "ju": "ju-hero.jpg",
}

CANTON_ADJ_F = {
    "ge": "genevoises",
    "vd": "vaudoises",
    "vs": "valaisannes",
    "fr": "fribourgeoises",
    "ne": "neuchâteloises",
    "ju": "jurassiennes",
}

CANTON_ADJ_M = {
    "ge": "genevois",
    "vd": "vaudois",
    "vs": "valaisans",
    "fr": "fribourgeois",
    "ne": "neuchâtelois",
    "ju": "jurassiens",
}

OTHER_GRID_RE = (
    r'<div class="other-grid">(?:\s*<a\b[^>]*\bclass="other-card"[^>]*>.*?</a>\s*)*\s*</div>'
)
COMMUNES_CLOUD_RE = (
    r'<div class="communes-cloud">(?:\s*<span class="commune-pill">.*?</span>\s*)*\s*</div>'
)

# Default communes per canton (fallback if PDF parse fails)
DEFAULT_COMMUNES = {
    "ge": ["Genève", "Carouge", "Meyrin", "Vernier", "Lancy", "Onex", "Thônex", "Bernex", "Grand-Saconnex", "Chêne-Bougeries", "Cologny", "Plan-les-Ouates", "Versoix"],
    "vd": ["Lausanne", "Montreux", "Nyon", "Yverdon-les-Bains", "Renens", "Morges", "Vevey", "Pully", "Gland", "Prilly", "Rolle", "Lutry"],
    "vs": ["Sion", "Martigny", "Sierre", "Monthey", "Saxon", "Visp", "Brig-Glis", "Conthey", "Naters", "Collombey-Muraz"],
    "fr": ["Fribourg", "Bulle", "Estavayer-le-Lac", "Murten", "Romont", "Villars-sur-Glâne", "Marly", "Düdingen"],
    "ne": ["Neuchâtel", "La Chaux-de-Fonds", "Le Locle", "Boudry", "Peseux", "Colombier", "Val-de-Travers"],
    "ju": ["Delémont", "Porrentruy", "Courrendlin", "Bassecourt", "Delemont", "Boncourt", "Courgenay"],
}


def pdftotext(path: str) -> str:
    try:
        out = subprocess.check_output(["pdftotext", path, "-"], stderr=subprocess.DEVNULL)
        return out.decode("utf-8", errors="replace")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def find_pdf(service: str, canton_key: str) -> str | None:
    pdf_name = CANTONS[canton_key]["pdf"]
    for pattern in SERVICES[service]["pdf_globs"]:
        matches = glob.glob(os.path.join(PDF_DIR, pattern.format(pdf=pdf_name)))
        if matches:
            return sorted(matches)[0]
    # fuzzy fallback
    slug = pdf_name.lower()
    for f in glob.glob(os.path.join(PDF_DIR, "*.pdf")):
        base = os.path.basename(f).lower()
        if slug in base and service[:4] in base.replace("debarras_", "debarras"):
            return f
    return None


def clean_text(s: str) -> str:
    s = s.replace("■", "-").replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_after_label(text: str, labels: list[str], max_len: int = 600) -> str | None:
    for label in labels:
        pat = rf"(?:^|\n){re.escape(label)}\s*\n(.{{10,{max_len}}}?)(?:\n\n|\n[A-Z][A-Z \-/]+(?:\n|$))"
        m = re.search(pat, text, re.I | re.S)
        if m:
            return clean_text(m.group(1))
    return None


def parse_pdf(text: str, service: str, canton_key: str) -> dict:
    c = CANTONS[canton_key]
    data: dict = {}

    title = extract_after_label(text, ["TITLE SEO", "Title SEO"])
    if title:
        data["title"] = title.replace("Val-Débarras", "Val-Débarras")

    meta = extract_after_label(text, ["META DESCRIPTION", "Meta description"])
    if meta:
        data["meta"] = meta

    h1 = extract_after_label(text, ["H1", "H1 conseillé"])
    if h1:
        data["h1"] = h1
    else:
        data["h1"] = f"{SERVICES[service]['h1_service']} {c['name']}"

    hero = extract_after_label(
        text,
        ["HERO TEXT", "HERO SECTION", "Accroche principale", "Accroche émotionnelle principale"],
        max_len=800,
    )
    if not hero:
        # nettoyage extreme: combine subtitle lines
        m = re.search(r"Sous■titre rassurant\s*\n(.+?)(?:\nChaque heure|\n•|\nCTA)", text, re.S)
        if m:
            hero = clean_text(m.group(1))
    if hero:
        data["hero_text"] = hero

    section = extract_after_label(text, ["SECTION PRINCIPALE"], max_len=900)
    if section:
        data["section_text"] = section

    # Communes from VILLES line or Zones à ajouter
    communes: list[str] = []
    m = re.search(rf"VILLES\s+{re.escape(c['pdf'].upper())}\s*\n(.+?)(?:\n\n|\nMOTS|\nINSTRUCTIONS|\Z)", text, re.S | re.I)
    if m:
        line = m.group(1).replace("\n", " ")
        parts = re.split(r",| ainsi que ", line)
        for p in parts:
            p = clean_text(p)
            if p and len(p) > 2 and "localités" not in p.lower() and "canton" not in p.lower():
                communes.append(p.rstrip("."))

    m2 = re.search(r"Zones à ajouter\s*\n((?:[^\n]+\n)+)", text)
    if m2:
        for line in m2.group(1).strip().split("\n"):
            line = clean_text(line)
            if line and len(line) > 2:
                communes.append(line)

    m3 = re.search(r"COMMUNES(?:\s+\w+)?\s*\n((?:[^\n]+\n)+)", text, re.I)
    if m3:
        for line in m3.group(1).strip().split("\n"):
            line = clean_text(line)
            if line and len(line) > 2 and not line.startswith("•"):
                communes.append(line)

    # dedupe preserving order
    seen = set()
    unique = []
    for city in communes:
        key = city.lower()
        if key not in seen:
            seen.add(key)
            unique.append(city)
    data["communes"] = unique[:14] if unique else DEFAULT_COMMUNES[canton_key]

    # FAQs
    faqs = []
    for i in range(1, 7):
        q = extract_after_label(text, [f"FAQ {i}"], max_len=200)
        a = extract_after_label(text, [f"RÉPONSE FAQ {i}", f"REPONSE FAQ {i}"], max_len=400)
        if q and a:
            faqs.append((q, a))
    if faqs:
        data["faqs"] = faqs

    return data


def build_communes_html(communes: list[str]) -> str:
    pills = "\n".join(f'      <span class="commune-pill">{c}</span>' for c in communes)
    return f'    <div class="communes-cloud">\n{pills}\n    </div>'


def build_other_services_html(canton_key: str, current_service: str) -> str:
    c = CANTONS[canton_key]
    cards = []
    for svc_key, url_path, title, desc, icon, *rest in ALL_OTHER_SERVICES:
        if svc_key == current_service:
            continue
        orange = rest[0] if rest else False
        icon_class = ' class="icon icon-orange"' if orange else ' class="icon"'
        href = f"/{url_path}/{c['slug']}/"
        cards.append(
            f'      <a href="{href}" class="other-card">\n'
            f'        <div class="other-card-icon"><svg{icon_class}><use href="#{icon}"/></svg></div>\n'
            f'        <h3 class="other-card-title">{title}</h3>\n'
            f'        <p class="other-card-desc">{desc}</p>\n'
            f'        <span class="other-card-cta">Devis →</span>\n'
            f'      </a>'
        )
    return "\n".join(cards)


def build_sidebar_cantons_html(canton_key: str, service: str) -> str:
    svc = SERVICES[service]
    items = []
    for ck, cv in CANTONS.items():
        if ck == canton_key:
            continue
        href = f"/{svc['url_path']}/{cv['slug']}/"
        shield = f"/images/shield-{ck}.svg"
        items.append(
            f'        <li><a href="{href}" style="display:flex;align-items:center;gap:10px;padding:8px 6px;border-radius:8px;font-size:14px;font-weight:600;color:var(--gris-fonce);transition:background .15s;" onmouseover="this.style.background=\'#f3f4f6\'" onmouseout="this.style.background=\'transparent\'"><img src="{shield}" class="canton-icon" alt="Écusson {cv["name"]}" loading="lazy"><span>{cv["prep"]}</span></a></li>'
        )
    return "\n".join(items)


def build_faq_html(faqs: list[tuple[str, str]]) -> str:
    items = []
    for q, a in faqs:
        items.append(
            f'    <div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)">{q} <span class="faq-arr">▾</span></button><div class="faq-a">{a}</div></div>'
        )
    return "\n".join(items)


def apply_canton_content(html: str, service: str, canton_key: str, pdf_data: dict) -> str:
    c = CANTONS[canton_key]
    svc = SERVICES[service]
    ge = CANTONS["ge"]

    # Title & meta
    title = pdf_data.get("title") or f"{svc['h1_service']} {c['prep']} | Val-Débarras"
    meta = pdf_data.get(
        "meta",
        f"{svc['h1_service']} {c['prep_in']}. Intervention rapide, devis gratuit.",
    )
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{meta}">',
        html,
        count=1,
    )

    # H1 — use prep with à/en/dans/au
    h1_raw = pdf_data.get("h1", f"{svc['h1_service']} {c['name']}")
    if c["prep"].startswith(("à ", "au ", "en ", "dans ", "sur ")):
        h1_display = f"{svc['h1_service']} {c['prep']}"
    else:
        h1_display = h1_raw
    html = re.sub(r"<h1>.*?</h1>", f"<h1>{h1_display}</h1>", html, count=1)

    # Hero subtitle & text
    hero_sub = svc["hero_sub_tpl"]
    html = re.sub(
        r'<div class="hero-sub-title">.*?</div>',
        f'<div class="hero-sub-title">{hero_sub}</div>',
        html,
        count=1,
    )
    hero_text = pdf_data.get(
        "hero_text",
        f"Val-Débarras intervient rapidement {c['prep_in']} pour {svc['breadcrumb'].lower()}. Devis gratuit et intervention professionnelle.",
    )
    html = re.sub(
        r'<p class="hero-text">.*?</p>',
        f'<p class="hero-text">{hero_text}</p>',
        html,
        count=1,
        flags=re.S,
    )

    # Section kicker & h2 & text
    html = re.sub(
        r'<span class="section-kicker">Notre service à Genève</span>',
        f'<span class="section-kicker">Notre service {c["prep"]}</span>',
        html,
        count=1,
    )
    section_h2 = svc["section_h2_tpl"].format(prep=c["prep"])
    html = re.sub(
        r'<h2 class="section-h2">.*?</h2>',
        f'<h2 class="section-h2">{section_h2}</h2>',
        html,
        count=1,
        flags=re.S,
    )
    section_text = pdf_data.get(
        "section_text",
        f"Nous intervenons {c['prep_in']} pour {svc['breadcrumb'].lower()}. Intervention rapide et devis gratuit.",
    )
    html = re.sub(
        r'<p class="section-text">.*?</p>',
        f'<p class="section-text">{section_text}</p>',
        html,
        count=1,
        flags=re.S,
    )

    # Breadcrumb canton
    html = html.replace(
        f'<img src="/images/shield-ge.svg" class="canton-icon" alt="Écusson Genève" loading="lazy">\n    <strong>Genève</strong>',
        f'<img src="/images/shield-{canton_key}.svg" class="canton-icon" alt="Écusson {c["name"]}" loading="lazy">\n    <strong>{c["name"]}</strong>',
    )

    # Communes section
    communes_heading = svc["communes_heading_tpl"].format(prep=c["prep"])
    html = re.sub(
        r"<h3>Communes couvertes à Genève</h3>",
        f"<h3>{communes_heading}</h3>",
        html,
        count=1,
    )
    html = re.sub(
        COMMUNES_CLOUD_RE,
        build_communes_html(pdf_data.get("communes", DEFAULT_COMMUNES[canton_key])),
        html,
        count=1,
        flags=re.S,
    )

    # Autres services heading & links
    html = re.sub(
        r"<h2>Autres services à Genève</h2>",
        f'<h2>Autres services {c["prep"]}</h2>',
        html,
        count=1,
    )
    html = re.sub(
        OTHER_GRID_RE,
        f'<div class="other-grid">\n{build_other_services_html(canton_key, service)}\n    </div>',
        html,
        count=1,
        flags=re.S,
    )

    # Sidebar canton switcher
    html = re.sub(
        r'(<ul style="list-style:none;">)\s*.*?\s*(</ul>)',
        rf"\1\n\n{build_sidebar_cantons_html(canton_key, service)}\n      \2",
        html,
        count=1,
        flags=re.S,
    )

    # Form canton pre-select
    for ck, cv in CANTONS.items():
        html = html.replace(f"<option selected>{cv['name']}</option>", f"<option>{cv['name']}</option>")
    html = html.replace(
        f"<option>{c['name']}</option>",
        f"<option selected>{c['name']}</option>",
        1,
    )

    # Form service pre-select
    for sk, sv in SERVICES.items():
        html = html.replace(f"<option selected>{sv['form_option']}</option>", f"<option>{sv['form_option']}</option>")
    html = html.replace(
        f"<option>{svc['form_option']}</option>",
        f"<option selected>{svc['form_option']}</option>",
        1,
    )

    # FAQ if available — also fix canton name in questions
    if pdf_data.get("faqs"):
        faqs = []
        for q, a in pdf_data["faqs"]:
            q = q.replace("à Genève", c["prep"]).replace("Genève", c["name"])
            a = a.replace("canton de Genève", f"canton {c['prep_in'].replace('dans le ', 'du ').replace('à ', 'd\'').replace('en ', 'd\'').replace('au ', 'du ')}")
            faqs.append((q, a))
        html = re.sub(
            r'(<div class="faq-inner">\s*<h2>Questions fréquentes</h2>\s*).*?(\s*</div>\s*</section>)',
            rf"\1\n{build_faq_html(faqs)}\n  \2",
            html,
            count=1,
            flags=re.S,
        )
    else:
        html = re.sub(
            r"à Genève \?",
            f"{c['prep']} ?",
            html,
        )
        html = re.sub(
            r"d'un débarras d'appartement à Genève",
            f"d'un débarras d'appartement {c['prep']}",
            html,
        )
        html = re.sub(
            r"dans le canton de Genève",
            c["prep_in"],
            html,
        )

    # Hero image (canton-specific when available)
    hero_img = HERO_IMAGES.get(canton_key, "ge-hero.jpg")
    html = re.sub(
        r'(<div class="hero-img">\s*<img src="/images/)[^"]+(" alt=")[^"]*(" loading="eager">)',
        rf'\1{hero_img}\2Val-Débarras — {svc["h1_service"]} {c["prep"]}\3',
        html,
        count=1,
    )

    # Pro-section & content: replace Geneva-specific wording (not nav labels)
    ge_adj_f, ge_adj_m = CANTON_ADJ_F["ge"], CANTON_ADJ_M["ge"]
    adj_f, adj_m = CANTON_ADJ_F[canton_key], CANTON_ADJ_M[canton_key]
    if canton_key != "ge":
        html = html.replace(f"régies immobilières {ge_adj_f}", f"régies immobilières {adj_f}")
        html = html.replace(f"régies {ge_adj_f}", f"régies {adj_f}")
        html = html.replace(f"EMS {ge_adj_m}", f"EMS {adj_m}")
        html = html.replace("successions à Genève", f"successions {c['prep']}")
        html = html.replace(
            "Intervention rapide dans tout le canton de Genève",
            f"Intervention rapide {c['prep_in']}",
        )
        html = html.replace(
            "à Genève-ville, Carouge, Meyrin, Vernier, Lancy et dans toutes les communes du canton",
            f"{c['prep_in']} et dans toutes les communes du canton",
        )
        html = html.replace("dans le canton de Genève", c["prep_in"])

    return html


def generate_page(service: str, canton_key: str, force: bool = False) -> tuple[str, bool]:
    if canton_key == "ge":
        return f"ge-{service}.html", False

    template_path = os.path.join(BASE, SERVICES[service]["template"])
    out_path = os.path.join(BASE, f"{canton_key}-{service}.html")

    with open(template_path, encoding="utf-8") as f:
        html = f.read()

    pdf_path = find_pdf(service, canton_key)
    pdf_data: dict = {}
    if pdf_path:
        text = pdftotext(pdf_path)
        pdf_data = parse_pdf(text, service, canton_key)
        print(f"  PDF: {os.path.basename(pdf_path)}")
    else:
        print(f"  ⚠ No PDF for {canton_key}-{service}, using defaults")

    html = apply_canton_content(html, service, canton_key, pdf_data)

    existing = ""
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            existing = f.read()

    if not force and html == existing:
        return os.path.basename(out_path), False

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.basename(out_path), True


def generate_vercel_rewrites() -> list[dict]:
    rewrites = [
        {"source": "/brand", "destination": "/brand.html"},
        {"source": "/blog", "destination": "/blog.html"},
        {"source": "/blog/", "destination": "/blog.html"},
        {
            "source": "/blog/comment-debarrasser-appartement-suisse-romande",
            "destination": "/blog-article-1.html",
        },
        {
            "source": "/blog/comment-debarrasser-appartement-suisse-romande/",
            "destination": "/blog-article-1.html",
        },
    ]
    for service, svc in SERVICES.items():
        for canton_key, c in CANTONS.items():
            dest = f"/{canton_key}-{service}.html"
            path = f"/{svc['url_path']}/{c['slug']}"
            rewrites.append({"source": path, "destination": dest})
            rewrites.append({"source": path + "/", "destination": dest})
    rewrites.append({"source": "/(.*)", "destination": "/index.html"})
    return rewrites


def main():
    import sys

    force = "--force" in sys.argv
    print("=== generate_canton_pages.py ===")
    if force:
        print("(force mode — rewriting all non-GE pages)")
    created = updated = 0
    missing_pdfs = []

    for service in SERVICES:
        for canton_key in CANTONS:
            if canton_key == "ge":
                continue
            print(f"\n→ {canton_key}-{service}")
            if not find_pdf(service, canton_key):
                missing_pdfs.append(f"{canton_key}-{service}")
            fname, changed = generate_page(service, canton_key, force=force)
            if changed:
                updated += 1
                print(f"  ✓ wrote {fname}")
            else:
                print(f"  ~ unchanged {fname}")

    vercel_path = os.path.join(BASE, "vercel.json")
    new_rewrites = generate_vercel_rewrites()
    vercel_data = {"rewrites": new_rewrites}
    with open(vercel_path, encoding="utf-8") as f:
        existing = json.load(f)
    if existing.get("rewrites") != new_rewrites:
        with open(vercel_path, "w", encoding="utf-8") as f:
            json.dump(vercel_data, f, indent=2)
            f.write("\n")
        print(f"\n✓ vercel.json updated ({len(new_rewrites)} rewrites)")
    else:
        print("\n~ vercel.json unchanged")

    print(f"\nDone: {updated} pages written/updated")
    if missing_pdfs:
        print(f"Missing PDFs ({len(missing_pdfs)}): {', '.join(missing_pdfs)}")


if __name__ == "__main__":
    main()
