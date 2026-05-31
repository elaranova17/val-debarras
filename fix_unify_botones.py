#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unificación de componentes — botones / tel / iconografía.

Hace que TODOS los botones de TODAS las secciones tengan la misma forma,
disposición y acciones que los del hero de index.html
(btn-phone / btn-devis / btn-services), estandariza los enlaces tel: y la
iconografía (📞 / 📋), e inyecta el CSS de botones del hero donde falte.

Referencia: hero actual de index.html (btn-phone simple, radius 12px).
Idempotente.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent

SERVICE_PAGES = [
    "ge-appartement.html", "ge-maison.html", "ge-succession.html",
    "ge-ems.html", "ge-diogene.html", "ge-nettoyage.html",
]

# ── Botones canónicos (idénticos al hero actual de index.html) ──────────────
BTN_PHONE = '<a href="tel:+41795805857" class="btn-phone">📞 079 580 58 57</a>'
def BTN_DEVIS(href="#devis"): return f'<a href="{href}" class="btn-devis">📋 Devis gratuit</a>'
def BTN_SERVICES(href="#services"): return f'<a href="{href}" class="btn-services">Nos services →</a>'

# CSS canónico de los botones del hero (igual que index.html)
CANON_BTN_CSS = """.btn-phone{
  display:inline-flex;align-items:center;gap:8px;
  background:white;color:var(--vert-fonce);
  padding:14px 22px;border-radius:12px;
  font-weight:800;font-size:15px;
  text-decoration:none;transition:all .22s;
  box-shadow:0 4px 16px rgba(0,0,0,.18);
  border:2px solid transparent;white-space:nowrap;
}
.btn-phone:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.22);}

.btn-devis{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--vert);color:white;
  padding:14px 22px;border-radius:12px;
  font-weight:800;font-size:15px;
  text-decoration:none;transition:all .22s;
  border:2px solid transparent;white-space:nowrap;
}
.btn-devis:hover{background:var(--vert-fonce);transform:translateY(-2px);}

.btn-services{
  display:inline-flex;align-items:center;gap:6px;
  background:transparent;color:rgba(255,255,255,.85);
  padding:14px 18px;border-radius:12px;
  font-weight:700;font-size:15px;
  text-decoration:none;transition:all .22s;
  border:2px solid rgba(255,255,255,.3);white-space:nowrap;
}"""

# Bloque completo para inyectar donde no exista nada (blog*)
HERO_BTN_CSS_FULL = (
    "\n/* ===== Botones del hero unificados ===== */\n"
    ".hero-btns{display:flex;gap:12px;flex-wrap:wrap;align-items:center;}\n"
    + CANON_BTN_CSS + "\n"
    ".btn-services:hover{transform:translateX(4px);}\n"
)

# CSS para los grupos en sidebar / pro
GROUP_CSS = (
    "\n/* ===== CTA groups unificados (sidebar / pro) ===== */\n"
    ".sidebar-cta{margin-top:14px;flex-direction:column;align-items:stretch;}\n"
    ".sidebar-cta .btn-phone,.sidebar-cta .btn-devis{justify-content:center;}\n"
    ".pro-cta{margin-top:6px;}\n"
)


def read(n): return (BASE / n).read_text(encoding="utf-8")
def write(n, t): (BASE / n).write_text(t, encoding="utf-8")


def align_btn_css(html):
    """Normaliza el CSS de btn-phone/devis/services al canónico del index."""
    pat = re.compile(
        r'\.btn-phone\{.*?\}\s*'
        r'\.btn-phone:hover\{.*?\}\s*'
        r'(?:\.btn-phone__[a-z]+\{.*?\}\s*)*'
        r'\.btn-devis\{.*?\}\s*'
        r'\.btn-devis:hover\{.*?\}\s*'
        r'\.btn-services\{.*?\}',
        re.DOTALL,
    )
    return pat.sub(lambda m: CANON_BTN_CSS, html, count=1)


def unify_service_hero(html):
    pat = re.compile(
        r'<div class="hero-btns">\s*'
        r'<a href="tel:0795805857" class="btn btn-white">.*?</div>',
        re.DOTALL,
    )
    new = (
        '<div class="hero-btns">\n'
        f'        {BTN_PHONE}\n'
        f'        {BTN_DEVIS("#devis")}\n'
        f'        {BTN_SERVICES("/#services")}\n'
        '      </div>'
    )
    return pat.sub(new, html, count=1)


def unify_sidebar(html):
    pat = re.compile(
        r'<a href="tel:0795805857" class="sidebar-phone">.*?</a>\s*'
        r'<a href="#devis" class="sidebar-btn">.*?</a>',
        re.DOTALL,
    )
    new = (
        '<div class="hero-btns sidebar-cta">\n'
        f'      {BTN_PHONE}\n'
        f'      {BTN_DEVIS("#devis")}\n'
        '    </div>'
    )
    return pat.sub(new, html, count=1)


def unify_pro(html):
    old = '<a href="#devis" class="btn-pro">Nous contacter →</a>'
    if old not in html:
        return html
    new = (
        '<div class="hero-btns pro-cta">'
        f'{BTN_PHONE} {BTN_DEVIS("#devis")}'
        '</div>'
    )
    return html.replace(old, new)


def unify_blog_cta(html):
    pat = re.compile(r'<div class="blog-cta-btns">.*?</div>', re.DOTALL)
    new = (
        '<div class="blog-cta-btns">\n'
        f'      {BTN_PHONE}\n'
        f'      {BTN_DEVIS("/#devis")}\n'
        f'      {BTN_SERVICES("/#services")}\n'
        '    </div>'
    )
    return pat.sub(new, html, count=1)


def unify_art_cta(html):
    old = '<a href="tel:0795805857">📞 Appeler le 079 580 58 57</a>'
    if old not in html:
        return html
    new = (
        '<div class="hero-btns" style="justify-content:center;">\n'
        f'      {BTN_PHONE}\n'
        f'      {BTN_DEVIS("/#devis")}\n'
        f'      {BTN_SERVICES("/#services")}\n'
        '    </div>'
    )
    return html.replace(old, new)


def inject_css_full(html):
    if '.btn-phone{' in html:
        return html
    return html.replace('</style>', HERO_BTN_CSS_FULL + '</style>', 1)


def inject_group_css(html):
    if '.sidebar-cta{' in html:
        return html
    return html.replace('</style>', GROUP_CSS + '</style>', 1)


def std_tel(html):
    return html.replace('tel:0795805857', 'tel:+41795805857')


def main():
    changed = []

    for page in SERVICE_PAGES:
        h = read(page); before = h
        h = align_btn_css(h)
        h = unify_service_hero(h)
        h = unify_sidebar(h)
        h = unify_pro(h)
        h = inject_group_css(h)
        h = std_tel(h)
        if h != before:
            write(page, h); changed.append(page)

    h = read("blog.html"); before = h
    h = inject_css_full(h)
    h = unify_blog_cta(h)
    h = std_tel(h)
    if h != before:
        write("blog.html", h); changed.append("blog.html")

    h = read("blog-article-1.html"); before = h
    h = inject_css_full(h)
    h = unify_art_cta(h)
    h = std_tel(h)
    if h != before:
        write("blog-article-1.html", h); changed.append("blog-article-1.html")

    h = read("index.html"); before = h
    h = std_tel(h)
    if h != before:
        write("index.html", h); changed.append("index.html")

    print("Páginas modificadas:", ", ".join(changed) if changed else "ninguna")


if __name__ == "__main__":
    main()
