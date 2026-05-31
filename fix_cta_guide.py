#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guide design — Phase 2 : CTAs (cartes services, hero micro-copy, sticky mobile).

Idempotent : relançable sur tous les *.html du prototype.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CTA_CSS = """
/* === CTA GUIDE VD === */
.btn-primary{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--vert);color:white;
  padding:12px 18px;border-radius:12px;
  font-weight:800;font-size:14px;
  text-decoration:none;transition:transform .25s ease,box-shadow .25s ease;
  border:none;cursor:pointer;font-family:var(--font);
  margin-top:18px;
}
.btn-primary:hover{background:var(--vert-fonce);}
.btn-primary .arrow-icon{width:16px;height:16px;transition:transform .25s ease;}

.link-secondary{
  display:inline-flex;align-items:center;gap:6px;
  font-size:12px;font-weight:600;color:rgba(255,255,255,.65);
  text-decoration:none;margin-top:10px;
  border-bottom:1px solid transparent;transition:color .2s,border-color .2s;
}
.link-secondary:hover{color:white;border-bottom-color:rgba(255,255,255,.45);}

.hero-micro{
  font-size:13px;color:rgba(255,255,255,.65);
  margin-top:14px;font-weight:500;letter-spacing:.01em;
}
.hero-micro--dark{color:var(--gris);margin-top:12px;}

.header-phone-pulse{position:relative;}
.header-phone-pulse::after{
  content:'';position:absolute;inset:-4px;border-radius:50%;
  border:2px solid rgba(0,155,116,.35);
  animation:vd-pulse-ring 2.5s ease-out infinite;
  pointer-events:none;
}
@keyframes vd-pulse-ring{
  0%{transform:scale(.85);opacity:.8;}
  70%,100%{transform:scale(1.35);opacity:0;}
}
@media(max-width:768px){.header-phone-pulse::after{display:none;}}

.sticky-mobile__devis{background:var(--gris-fonce);}
"""

HERO_MICRO = '<p class="hero-micro">Réponse sous 2h — Intervention dès demain</p>'

STICKY_HTML = """
<!-- STICKY BAR MOBILE (guide VD) -->
<div class="sticky-mobile" id="stickyBar">
  <a href="tel:+41795805857" class="sticky-mobile__call"><svg class="icon icon-btn"><use href="#icon-phone-line"/></svg>Appeler</a>
  <a href="#devis" class="sticky-mobile__devis"><svg class="icon icon-btn"><use href="#icon-document-line"/></svg>Devis gratuit — 24h</a>
</div>
"""

STICKY_JS = """
<script>
(function(){
  var bar=document.getElementById('stickyBar');
  if(!bar)return;
  var last=0;
  setTimeout(function(){bar.classList.add('visible');},800);
  window.addEventListener('scroll',function(){
    var cur=window.pageYOffset;
    if(cur>last&&cur>200){bar.classList.remove('visible');}
    else{bar.classList.add('visible');}
    last=cur;
  },{passive:true});
})();
</script>"""

SERVICE_LINKS = {
    "Débarras appartement": "/debarras-appartement/geneve/",
    "Débarras maison": "/debarras-maison/geneve/",
    "Débarras après décès & succession": "/debarras-apres-deces/geneve/",
    "Débarras suite entrée en EMS": "/debarras-ems/geneve/",
    "Débarras insalubre / Diogène": "/debarras-insalubre-diogene/geneve/",
    "Nettoyages extrême": "/nettoyage-extreme/geneve/",
}


def inject_css(html):
    if "CTA GUIDE VD" in html:
        return html
    return html.replace("</style>", CTA_CSS + "\n</style>", 1)


def fix_index_service_cards(html):
    if 'class="services-grid"' not in html:
        return html
    for svc, href in SERVICE_LINKS.items():
        # Primary CTA before toggle/link block
        primary = (
            f'<a href="#devis" class="btn-primary sc-card-primary" data-select="{svc}">'
            f'<svg class="icon icon-btn"><use href="#icon-document-line"/></svg>'
            f'Devis gratuit — 24h'
            f'<svg class="icon icon-btn arrow-icon"><use href="#icon-arrow-right"/></svg></a>'
        )
        secondary = (
            f'<a href="{href}" class="link-secondary sc-link">'
            f'Voir les zones d\'intervention →</a>'
        )
        pat = (
            rf'(<div class="sc" data-service="{re.escape(svc)}">.*?'
            rf'(<button class="sc-toggle"[^>]*>.*?</button>)\s*)'
            rf'(<a href="[^"]*" class="sc-link">[^<]*</a>)'
        )
        repl = rf"\1{primary}\n        {secondary}\n        "
        html = re.sub(pat, repl, html, count=1, flags=re.S)
    return html


def fix_hero_micro(html):
    if 'class="hero-micro"' in html:
        return html
    html = re.sub(
        r'(<div class="hero-btns">.*?</div>)(\s*</div>\s*<div class="hero-img">)',
        rf"\1\n      {HERO_MICRO}\2",
        html,
        count=1,
        flags=re.S,
    )
    return html


def fix_sticky(html):
    if "stickyBar" in html:
        html = re.sub(
            r'(<a href="#devis" class="sticky-mobile__devis"[^>]*>)(.*?)(</a>)',
            r'\1<svg class="icon icon-btn"><use href="#icon-document-line"/></svg>Devis gratuit — 24h\3',
            html,
            count=1,
            flags=re.S,
        )
        return html
    if "STICKY BAR MOBILE" in html:
        return html
    block = STICKY_HTML + STICKY_JS
    return html.replace("</body>", block + "\n</body>", 1)


def fix_header_pulse(html):
    if "header-phone-pulse" in html:
        return html
    html = re.sub(
        r'(<a href="tel:\+41795805857" class="header-phone")',
        r'<a href="tel:+41795805857" class="header-phone header-phone-pulse"',
        html,
        count=1,
    )
    return html


def fix_other_card_cta(html):
    return html.replace(
        '<span class="other-card-cta">Devis →</span>',
        '<span class="other-card-cta">Devis '
        '<svg class="icon icon-sm arrow-icon"><use href="#icon-arrow-right"/></svg></span>',
    )


def process(html, fname):
    html = inject_css(html)
    if fname == "index.html":
        html = fix_index_service_cards(html)
    html = fix_hero_micro(html)
    html = fix_sticky(html)
    html = fix_header_pulse(html)
    html = fix_other_card_cta(html)
    return html


def main():
    changed = []
    for path in sorted(ROOT.glob("*.html")):
        orig = path.read_text(encoding="utf-8")
        new = process(orig, path.name)
        if new != orig:
            path.write_text(new, encoding="utf-8")
            changed.append(path.name)
    print(f"fix_cta_guide.py — {len(changed)} page(s) modifiée(s)")


if __name__ == "__main__":
    main()
