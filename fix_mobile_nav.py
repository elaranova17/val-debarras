#!/usr/bin/env python3
"""Inject hamburger drawer nav + mobile layout fixes on all site HTML pages. Idempotent."""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).parent
CSS_MARKER = "/* === MOBILE NAV VD === */"
CSS_END = "/* === END MOBILE NAV VD === */"
JS_MARKER = "/* === VD MOBILE NAV JS === */"
JS_END = "/* === END VD MOBILE NAV JS === */"

HTML_FILES = sorted(BASE.glob("*.html"))

CANTONS = [
    ("geneve", "ge", "à Genève"),
    ("vaud", "vd", "sur Vaud"),
    ("valais", "vs", "en Valais"),
    ("fribourg", "fr", "à Fribourg"),
    ("neuchatel", "ne", "à Neuchâtel"),
    ("jura", "ju", "au Jura"),
]

SERVICES = [
    ("Débarras appartement", "/debarras-appartement/{slug}/"),
    ("Débarras maison", "/debarras-maison/{slug}/"),
    ("Après décès &amp; succession", "/debarras-apres-deces/{slug}/"),
    ("Entrée en EMS", "/debarras-ems/{slug}/"),
    ("Diogène &amp; insalubre", "/debarras-insalubre-diogene/{slug}/"),
    ("Nettoyage extrême", "/nettoyage-extreme/{slug}/"),
]

MOBILE_NAV_CSS = f"""{CSS_MARKER}
/* Overlay + panneau latéral */
.drawer-overlay{{
  position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:499;
  opacity:0;visibility:hidden;pointer-events:none;
  transition:opacity .3s ease,visibility .3s;
}}
.drawer-overlay.is-open{{
  opacity:1;visibility:visible;pointer-events:auto;
}}
.mobile-drawer{{
  display:flex !important;flex-direction:column;
  position:fixed !important;top:0 !important;right:0 !important;bottom:0 !important;
  left:auto !important;width:min(85vw,320px) !important;max-width:320px;
  background:var(--blanc);z-index:500;overflow-y:auto;
  transform:translateX(100%);visibility:hidden;
  transition:transform .35s cubic-bezier(.16,1,.3,1),visibility .35s;
  box-shadow:-8px 0 32px rgba(0,0,0,.15);
}}
.mobile-drawer.is-open{{
  transform:translateX(0);visibility:visible;
}}
.drawer-header{{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 16px;border-bottom:1px solid #f3f4f6;flex-shrink:0;
}}
.drawer-close{{
  background:none;border:none;cursor:pointer;
  min-width:44px;min-height:44px;display:flex;align-items:center;justify-content:center;
  color:var(--gris-fonce);padding:0;
}}
.drawer-close .icon{{width:22px;height:22px;}}
.drawer-body{{padding:8px 16px 24px;flex:1;}}
.drawer-group{{border-bottom:1px solid #f3f4f6;}}
.drawer-title{{
  display:flex;justify-content:space-between;align-items:center;
  padding:14px 4px;font-size:15px;font-weight:700;cursor:pointer;
  min-height:48px;gap:8px;
}}
.drawer-title .arr,.drawer-title span{{pointer-events:none;}}
.drawer-title .arr{{display:inline-flex;color:var(--vert);transition:transform .2s;}}
.drawer-title.open .arr{{transform:rotate(180deg);}}
.drawer-cantons{{display:none;padding:0 0 10px 4px;}}
.drawer-cantons.open{{display:block;}}
.drawer-cantons a{{
  display:flex;align-items:center;gap:10px;
  padding:12px 8px;font-size:15px;border-radius:8px;min-height:44px;
}}
.drawer-cantons a:hover{{background:var(--gris-bg);}}
.drawer-cantons .canton-icon{{width:22px;height:28px;}}
.drawer-actions{{margin-top:16px;display:flex;flex-direction:column;gap:10px;}}
.drawer-phone{{
  display:flex;align-items:center;justify-content:center;gap:10px;
  background:var(--vert);color:white;padding:16px;border-radius:12px;
  font-weight:800;font-size:17px;min-height:52px;text-decoration:none;
}}
.drawer-devis{{
  display:flex;align-items:center;justify-content:center;gap:8px;
  background:var(--gris-fonce);color:white;padding:14px;border-radius:12px;
  font-weight:700;font-size:15px;min-height:48px;text-decoration:none;
}}

/* Header mobile : logo | téléphone compact | hamburger */
.header-inner{{padding:0 12px !important;gap:8px !important;height:60px !important;}}
.logo{{margin-right:auto !important;flex-shrink:0;}}
.logo-img{{width:48px !important;}}
.header-actions{{
  display:none;align-items:center;gap:6px;flex-shrink:0;margin-left:auto;
}}
.header-phone-compact{{
  display:flex;align-items:center;justify-content:center;
  width:44px;height:44px;border-radius:10px;
  background:var(--vert-clair);color:var(--vert-fonce);
  text-decoration:none;flex-shrink:0;
}}
.header-phone-compact .icon{{width:22px;height:22px;}}
.hamburger{{
  display:none;align-items:center;justify-content:center;
  width:44px;height:44px;min-width:44px;min-height:44px;
  background:none;border:none;cursor:pointer;padding:0;
  border-radius:10px;color:var(--gris-fonce);flex-shrink:0;
}}
.hamburger .hamburger-icon{{width:24px;height:24px;}}
.hamburger.open .hamburger-icon{{opacity:.85;}}

@media (max-width: 1024px) {{
  .nav{{display:none !important;}}
  .header-cta{{display:none !important;}}
  .header-actions{{display:flex !important;}}
  .hamburger{{display:flex !important;}}
}}
@media (min-width: 1025px) {{
  .header-actions{{display:none !important;}}
  .header-cta{{display:flex !important;}}
  .hamburger{{display:none !important;}}
  .nav{{display:flex !important;}}
}}

@media (max-width: 768px) {{
  html,body{{overflow-x:hidden;max-width:100vw;}}
  body.nav-open{{overflow:hidden;}}
  body.has-sticky-mobile{{padding-bottom:88px;}}

  .hero-desktop{{display:none !important;}}
  .hero-img{{display:none !important;}}

  .stats-inner{{grid-template-columns:repeat(2,1fr) !important;}}
  .stat{{padding:18px 12px !important;}}
  .stat-n{{font-size:28px !important;}}

  .services-grid{{grid-template-columns:1fr !important;}}
  .sc{{min-height:auto !important;}}
  .canton-grid,.cpill-row{{display:grid !important;grid-template-columns:repeat(2,1fr) !important;gap:10px !important;}}
  .canton-btn,.cpill{{width:100% !important;min-width:0 !important;}}
  .btn-phone,.btn-devis,.btn,.header-cta,.drawer-phone,.drawer-devis,
  .sticky-mobile__call,.sticky-mobile__devis{{
    min-height:48px;
  }}

  .sticky-mobile{{padding:10px 12px calc(12px + env(safe-area-inset-bottom,0px));}}
  .back-to-top{{bottom:calc(88px + env(safe-area-inset-bottom,0px));}}
}}

@media (prefers-reduced-motion: reduce) {{
  .drawer-overlay,.mobile-drawer,.sticky-mobile,.hamburger .hamburger-icon{{
    transition:none !important;
  }}
}}
{CSS_END}
"""

MOBILE_NAV_JS_BODY = f"""{JS_MARKER}
(function(){{
  var ham=document.getElementById('ham');
  var drawer=document.getElementById('drawer');
  var overlay=document.getElementById('drawerOverlay');
  var closeBtn=document.getElementById('drawerClose');
  if(!ham||!drawer) return;

  var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setOpen(open){{
    ham.classList.toggle('open',open);
    drawer.classList.toggle('is-open',open);
    drawer.classList.toggle('open',open);
    if(overlay) overlay.classList.toggle('is-open',open);
    document.body.classList.toggle('nav-open',open);
    document.body.style.overflow=open?'hidden':'';
    ham.setAttribute('aria-expanded',open?'true':'false');
    drawer.setAttribute('aria-hidden',open?'false':'true');
    if(overlay) overlay.setAttribute('aria-hidden',open?'false':'true');
  }}

  function closeMenu(){{ setOpen(false); }}

  ham.addEventListener('click',function(){{
    setOpen(!drawer.classList.contains('is-open'));
  }});
  if(closeBtn) closeBtn.addEventListener('click',closeMenu);
  if(overlay) overlay.addEventListener('click',closeMenu);

  drawer.querySelectorAll('.drawer-cantons a').forEach(function(a){{
    a.addEventListener('click',closeMenu);
  }});
  var devis=drawer.querySelector('.drawer-devis');
  if(devis) devis.addEventListener('click',closeMenu);

  document.addEventListener('keydown',function(e){{
    if(e.key==='Escape'&&drawer.classList.contains('is-open')) closeMenu();
  }});

  window.toggleDrawer=function(el){{
    var panel=el.nextElementSibling;
    if(!panel) return;
    var isOpen=panel.classList.contains('open');
    document.querySelectorAll('.drawer-cantons.open').forEach(function(p){{p.classList.remove('open');}});
    document.querySelectorAll('.drawer-title.open').forEach(function(t){{t.classList.remove('open');t.setAttribute('aria-expanded','false');}});
    if(!isOpen){{ panel.classList.add('open'); el.classList.add('open'); el.setAttribute('aria-expanded','true'); }}
  }};

  drawer.querySelectorAll('.drawer-title').forEach(function(btn){{
    btn.addEventListener('click',function(){{ window.toggleDrawer(btn); }});
  }});

  document.body.classList.add('has-sticky-mobile');
}})();
{JS_END}"""

MOBILE_NAV_SCRIPT = f"<script>\n{MOBILE_NAV_JS_BODY}\n</script>"

HAMBURGER_RE = re.compile(
    r'<button\s+class="hamburger"\s+id="ham"[^>]*>.*?</button>',
    re.DOTALL | re.IGNORECASE,
)

HEADER_ACTIONS = """<div class="header-actions">
    <a href="tel:+41795805857" class="header-phone-compact phone-animate" aria-label="Appeler le 079 580 58 57"><svg class="icon icon-btn" aria-hidden="true"><use href="#icon-phone-line"/></svg></a>
    <button type="button" class="hamburger" id="ham" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="drawer"><svg class="icon hamburger-icon" aria-hidden="true"><use href="#icon-menu"/></svg></button>
  </div>"""

OLD_HAM_SCRIPTS = [
    re.compile(
        r"<script>\s*// Hamburger\s*const ham[\s\S]*?function toggleDrawer\(el\)[\s\S]*?\}\s*</script>",
        re.IGNORECASE,
    ),
    re.compile(
        r"<script>\s*const ham=document\.getElementById\('ham'\)[\s\S]*?</script>",
        re.IGNORECASE,
    ),
]

JS_BLOCK_RE = re.compile(
    r"<script>\s*(?:<script>\s*)*"
    + re.escape(JS_MARKER)
    + r"[\s\S]*?"
    + re.escape(JS_END)
    + r"\s*</script>",
    re.IGNORECASE,
)

CORRUPT_SCRIPT_RE = re.compile(r"(?:<script>\s*)+(?=/\* === VD MOBILE NAV JS)", re.I)

CSS_BLOCK_RE = re.compile(
    re.escape(CSS_MARKER) + r"[\s\S]*?" + re.escape(CSS_END),
    re.IGNORECASE,
)


def canton_links(base_path: str) -> str:
    lines = []
    for slug, shield, label in CANTONS:
        href = base_path.format(slug=slug)
        lines.append(
            f'        <a href="{href}"><img src="/images/shield-{shield}.svg" class="canton-icon" '
            f'alt="Écusson {label.strip()}" loading="lazy"><span class="menu-label">{label}</span></a>'
        )
    return "\n".join(lines)


def build_drawer_html() -> str:
    groups = []
    for title, path_tpl in SERVICES:
        links = canton_links(path_tpl)
        groups.append(
            f"""    <div class="drawer-group">
      <button type="button" class="drawer-title" aria-expanded="false">{title} <span class="arr"><svg class="icon" aria-hidden="true"><use href="#icon-chevron-down"/></svg></span></button>
      <div class="drawer-cantons">
{links}
      </div>
    </div>"""
        )
    body = "\n".join(groups)
    return f"""<div class="drawer-overlay" id="drawerOverlay" aria-hidden="true"></div>
<div class="mobile-drawer" id="drawer" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Menu de navigation">
  <div class="drawer-header">
    <a href="/" class="logo" style="gap:10px;"><img src="/images/logo-icon.png" alt="Val-Débarras" class="logo-img" style="width:40px;height:auto;"></a>
    <button type="button" class="drawer-close" id="drawerClose" aria-label="Fermer le menu"><svg class="icon" aria-hidden="true"><use href="#icon-close"/></svg></button>
  </div>
  <div class="drawer-body">
{body}
    <div class="drawer-actions">
      <a href="tel:+41795805857" class="drawer-phone phone-animate"><svg class="icon icon-btn"><use href="#icon-phone-line"/></svg>079 580 58 57</a>
      <a href="#devis" class="drawer-devis"><svg class="icon icon-btn"><use href="#icon-document-line"/></svg>Devis gratuit — 24h</a>
    </div>
  </div>
</div>"""


def find_div_block_end(html: str, start: int) -> int:
    depth = 0
    i = start
    n = len(html)
    while i < n:
        if html.startswith("<div", i):
            depth += 1
            i += 4
            continue
        if html.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return i
            continue
        i += 1
    return n


def remove_orphan_mobile_nav(html: str) -> str:
    """Strip drawer/JS mistakenly added to non-site pages (e.g. brand.html)."""
    if "id=\"ham\"" in html:
        return html
    html = re.sub(
        r'<div class="drawer-overlay"[^>]*></div>\s*<div class="mobile-drawer" id="drawer"[\s\S]*?</div>\s*',
        "",
        html,
        count=1,
    )
    html = JS_BLOCK_RE.sub("", html)
    return html


def replace_drawer(html: str, drawer_html: str) -> tuple[str, bool]:
    if not is_site_page(html):
        cleaned = remove_orphan_mobile_nav(html)
        return cleaned, cleaned != html

    overlay_re = re.compile(
        r'<div class="drawer-overlay"[^>]*></div>\s*', re.IGNORECASE
    )
    m = re.search(r'<div class="mobile-drawer" id="drawer"', html, re.I)
    if not m:
        ins = re.search(
            r'<header class="header"[^>]*>[\s\S]*?</header>',
            html,
            re.I,
        )
        if not ins:
            return html, False
        pos = ins.end()
        new = html[:pos] + "\n\n" + drawer_html + "\n" + html[pos:]
        return new, True

    start = m.start()
    ov = list(overlay_re.finditer(html[:start]))
    if ov and ov[-1].end() >= start - 5:
        start = ov[-1].start()
    end = find_div_block_end(html, m.start())
    existing = html[start:end].strip()
    if existing == drawer_html.strip():
        return html, False
    new = html[:start] + drawer_html + "\n" + html[end:]
    return new, new != html


def patch_header_actions(html: str) -> tuple[str, bool]:
    if 'class="header-actions"' in html:
        html = HAMBURGER_RE.sub(
            '<button type="button" class="hamburger" id="ham" aria-label="Ouvrir le menu" '
            'aria-expanded="false" aria-controls="drawer">'
            '<svg class="icon hamburger-icon" aria-hidden="true"><use href="#icon-menu"/></svg></button>',
            html,
            count=1,
        )
        return html, False

    if not HAMBURGER_RE.search(html):
        return html, False

    html = HAMBURGER_RE.sub(HEADER_ACTIONS.strip(), html, count=1)
    if "desktop-only-phone" not in html:
        html = re.sub(
            r'(<a href="tel:\+41795805857" class=")(header-cta[^"]*)(")',
            r"\1\2 desktop-only-phone\3",
            html,
            count=1,
        )
    return html, True


def patch_drawer_titles(html: str) -> str:
    """Convert onclick drawer titles to buttons wired by JS."""
    html = re.sub(
        r'<div class="drawer-title" onclick="toggleDrawer\(this\)">',
        '<button type="button" class="drawer-title" aria-expanded="false">',
        html,
    )
    html = re.sub(
        r'</span></div>\s*\n\s*<div class="drawer-cantons">',
        '</span></button>\n      <div class="drawer-cantons">',
        html,
    )
    return html


def is_site_page(html: str) -> bool:
    return 'class="header"' in html and "header-inner" in html


def inject_css(html: str, full: bool = True) -> tuple[str, bool]:
    block = (MOBILE_NAV_CSS if full else BRAND_MOBILE_CSS).strip()
    if CSS_MARKER in html:
        m = CSS_BLOCK_RE.search(html)
        if m and m.group(0).strip() == block:
            return html, False
        new = CSS_BLOCK_RE.sub(block, html, count=1)
        return new, new != html
    if "</style>" not in html:
        return html, False
    new = html.replace("</style>", block + "\n</style>", 1)
    return new, True


BRAND_MOBILE_CSS = f"""{CSS_MARKER}
@media (max-width: 768px) {{
  html,body{{overflow-x:hidden;max-width:100vw;}}
  .bnav{{padding:0 1rem;}}
}}
{CSS_END}
"""


def inject_js(html: str) -> tuple[str, bool]:
    if not is_site_page(html) or 'id="ham"' not in html:
        cleaned = JS_BLOCK_RE.sub("", html)
        for pat in OLD_HAM_SCRIPTS:
            cleaned = pat.sub("", cleaned)
        return cleaned, cleaned != html

    for pat in OLD_HAM_SCRIPTS:
        html = pat.sub("", html)

    html = CORRUPT_SCRIPT_RE.sub("<script>\n", html)

    script = MOBILE_NAV_SCRIPT.strip()
    if JS_MARKER in html:
        m = JS_BLOCK_RE.search(html)
        if m and m.group(0).strip() == script:
            return html, False
        if m:
            new = JS_BLOCK_RE.sub(script, html, count=1)
            return new, new != html

    sticky = re.search(r'<div class="sticky-mobile"', html)
    if sticky:
        new = html[: sticky.start()] + MOBILE_NAV_SCRIPT + "\n\n" + html[sticky.start() :]
        return new, True
    new = html.replace("</body>", MOBILE_NAV_SCRIPT + "\n</body>", 1)
    return new, True


def process_file(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    orig = html
    changes: list[str] = []
    site = is_site_page(html)

    html, ok = inject_css(html, full=site)
    if ok:
        changes.append("css")

    drawer_html = build_drawer_html()
    html, ok = replace_drawer(html, drawer_html)
    if ok:
        changes.append("drawer")

    if site:
        html = patch_drawer_titles(html)
        html, ok = patch_header_actions(html)
        if ok:
            changes.append("header")
        html, ok = inject_js(html)
        if ok:
            changes.append("js")
    else:
        html, ok = inject_js(html)
        if ok:
            changes.append("js-cleanup")

    if html != orig:
        path.write_text(html, encoding="utf-8")
    return changes


def main() -> None:
    touched = []
    for path in HTML_FILES:
        ch = process_file(path)
        if ch:
            touched.append(f"{path.name}: {', '.join(ch)}")
    print(f"Pages mises à jour: {len(touched)}")
    for line in touched:
        print(f"  - {line}")


if __name__ == "__main__":
    main()
