#!/usr/bin/env python3
"""
fix_footer.py — Remplace le footer dans tous les fichiers HTML
Nouveau footer : mapa SVG sutil + 3 columnas + bottom bar
"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

# ── New Footer CSS ────────────────────────────────────────────────
NEW_FOOTER_CSS = """
/* ============================================================ */
/* FOOTER v2 — mapa + contacto + badges                         */
/* ============================================================ */
.footer{background:#0f172a;color:#94a3b8;font-family:var(--font);padding:0;}
.footer__map{position:relative;padding:48px 24px 32px;overflow:hidden;border-bottom:1px solid #1e293b;}
.footer__map-svg{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:600px;height:400px;opacity:0.07;pointer-events:none;z-index:0;}
.footer__locations{position:relative;z-index:1;display:flex;justify-content:center;gap:36px;flex-wrap:wrap;max-width:700px;margin:0 auto;}
.location-dot{display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;transition:all .3s ease;}
.location-dot:hover{transform:translateY(-4px);}
.location-dot__point{width:12px;height:12px;background:var(--vert);border-radius:50%;position:relative;transition:all .3s ease;}
.location-dot__point::before{content:'';position:absolute;inset:-6px;border:2px solid var(--vert);border-radius:50%;opacity:0;transition:all .3s ease;}
.location-dot:hover .location-dot__point::before{opacity:.4;inset:-10px;}
.location-dot--hq .location-dot__point{width:16px;height:16px;background:#22c55e;box-shadow:0 0 20px rgba(34,197,94,.4);}
.location-dot__label{font-size:12px;font-weight:500;color:#64748b;transition:color .3s ease;}
.location-dot:hover .location-dot__label{color:#dcfce7;}
.footer__content{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:48px;max-width:1200px;margin:0 auto;padding:48px 24px;position:relative;z-index:1;}
.footer__brand{display:flex;flex-direction:column;gap:16px;}
.footer__logo{display:flex;align-items:center;gap:12px;text-decoration:none;}
.footer__logo-img{width:40px;height:24px;object-fit:cover;object-position:left top;border-radius:4px;background:transparent;}
.footer__logo-text{display:flex;flex-direction:column;}
.footer__logo-brand{font-size:17px;font-weight:800;color:#fff;line-height:1.2;}
.footer__logo-suffix{font-size:12px;color:#64748b;}
.footer__desc{font-size:14px;line-height:1.75;color:#64748b;max-width:280px;}
.footer__contact{display:flex;flex-direction:column;gap:18px;}
.footer__title{font-size:11px;font-weight:700;color:#22c55e;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;}
.footer__phone{display:inline-flex;align-items:center;gap:10px;padding:12px 20px;background:var(--vert);color:#fff;font-size:16px;font-weight:800;border-radius:8px;text-decoration:none;transition:all .25s ease;width:fit-content;}
.footer__phone:hover{background:var(--vert-fonce);transform:translateY(-2px);box-shadow:0 8px 24px rgba(46,125,92,.35);}
.footer__email{display:flex;align-items:center;gap:8px;color:#94a3b8;font-size:14px;text-decoration:none;transition:color .2s;}
.footer__email:hover{color:#22c55e;}
.footer__address{display:flex;flex-direction:column;gap:4px;font-size:14px;color:#64748b;line-height:1.6;}
.footer__hours{display:flex;align-items:center;gap:8px;font-size:13px;color:#475569;}
.footer__badges{display:flex;flex-direction:column;gap:14px;}
.footer__badge{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;background:rgba(46,125,92,.1);border:1px solid rgba(46,125,92,.2);border-radius:100px;font-size:13px;font-weight:600;color:#4ade80;width:fit-content;text-decoration:none;transition:all .25s ease;}
.footer__badge:hover{background:rgba(46,125,92,.2);transform:translateX(4px);}
.footer__links{display:flex;flex-direction:column;gap:8px;margin-top:8px;}
.footer__link{font-size:13px;color:#64748b;text-decoration:none;transition:color .2s;}
.footer__link:hover{color:#94a3b8;}
.footer__bottom{border-top:1px solid #1e293b;padding:20px 24px;display:flex;justify-content:space-between;align-items:center;max-width:1200px;margin:0 auto;font-size:12px;color:#475569;}
.footer__bottom-links{display:flex;gap:20px;}
.footer__bottom-link{color:#475569;text-decoration:none;transition:color .2s;}
.footer__bottom-link:hover{color:#94a3b8;}
@media(max-width:768px){
  .footer__content{grid-template-columns:1fr;gap:36px;text-align:center;}
  .footer__brand,.footer__contact,.footer__badges{align-items:center;}
  .footer__desc{max-width:100%;}
  .footer__locations{gap:20px;}
  .footer__bottom{flex-direction:column;gap:12px;text-align:center;}
}
"""

# ── New Footer HTML ───────────────────────────────────────────────
NEW_FOOTER_HTML = """<footer class="footer">

  <!-- Mapa sutil Suisse romande -->
  <div class="footer__map">
    <svg class="footer__map-svg" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M50,80 Q80,60 120,70 Q160,50 200,65 Q240,45 280,60 Q320,50 350,80 Q360,120 340,150 Q350,200 320,230 Q280,250 240,240 Q200,260 160,250 Q120,260 80,240 Q50,220 60,180 Q40,140 50,80Z" fill="#334155" stroke="#475569" stroke-width="2"/>
      <path d="M120,150 L200,140 L280,160" stroke="#22c55e" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>
      <path d="M200,140 L200,200" stroke="#22c55e" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>
    </svg>
    <div class="footer__locations">
      <div class="location-dot" title="Valais"><span class="location-dot__point"></span><span class="location-dot__label">Valais</span></div>
      <div class="location-dot" title="Vaud"><span class="location-dot__point"></span><span class="location-dot__label">Vaud</span></div>
      <div class="location-dot location-dot--hq" title="Genève"><span class="location-dot__point"></span><span class="location-dot__label">Genève</span></div>
      <div class="location-dot" title="Fribourg"><span class="location-dot__point"></span><span class="location-dot__label">Fribourg</span></div>
      <div class="location-dot" title="Neuchâtel"><span class="location-dot__point"></span><span class="location-dot__label">Neuchâtel</span></div>
      <div class="location-dot" title="Jura"><span class="location-dot__point"></span><span class="location-dot__label">Jura</span></div>
    </div>
  </div>

  <!-- Contenido principal -->
  <div class="footer__content">

    <!-- Col 1: Logo + descripción -->
    <div class="footer__brand">
      <a href="/" class="footer__logo">
        <img src="/images/logo.jpg" alt="Val-Débarras" class="footer__logo-img">
        <div class="footer__logo-text">
          <span class="footer__logo-brand">Val-Débarras</span>
          <span class="footer__logo-suffix">Sàrl · Débarras & nettoyage</span>
        </div>
      </a>
      <p class="footer__desc">Entreprise active dans toute la Suisse romande depuis plus de 10 ans. Débarras, succession, EMS, nettoyage extrême.</p>
    </div>

    <!-- Col 2: Contact -->
    <div class="footer__contact">
      <h3 class="footer__title">Contact</h3>
      <a href="tel:+41795805857" class="footer__phone">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        079 580 58 57
      </a>
      <a href="mailto:info@val-debarras.ch" class="footer__email">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        info@val-debarras.ch
      </a>
      <div class="footer__address">
        <span>📍 Rue de Mazerette 9</span>
        <span>1950 Sion · Valais</span>
      </div>
      <div class="footer__hours">
        <span>🕐</span>
        <span>Lun–Sam · 08h00–18h00</span>
      </div>
    </div>

    <!-- Col 3: Services + links -->
    <div class="footer__badges">
      <h3 class="footer__title">Services</h3>
      <a href="/debarras-appartement/geneve/" class="footer__badge">🏠 Débarras appartement</a>
      <a href="/debarras-apres-deces/geneve/" class="footer__badge">🕊️ Après décès/succession</a>
      <a href="/debarras-ems/geneve/" class="footer__badge">🏥 Suite entrée EMS</a>
      <a href="/debarras-insalubre-diogene/geneve/" class="footer__badge">⚠️ Insalubre/Diogène</a>
      <a href="/nettoyage-extreme/geneve/" class="footer__badge">🧹 Nettoyages extrême</a>
      <div class="footer__links">
        <a href="/blog/" class="footer__link">Blog & conseils</a>
        <a href="#" class="footer__link">Protection des données</a>
        <a href="#" class="footer__link">Conditions générales</a>
        <a href="/brand" class="footer__link" style="color:var(--vert);font-weight:600;">🎨 Charte graphique</a>
      </div>
    </div>

  </div>

  <!-- Bottom bar -->
  <div class="footer__bottom">
    <span>© 2026 Val-Débarras Sàrl — Tous droits réservés</span>
    <div class="footer__bottom-links">
      <a href="#" class="footer__bottom-link">Mentions légales</a>
      <a href="#" class="footer__bottom-link">Plan du site</a>
    </div>
  </div>

</footer>"""

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
    'blog.html','blog-article-1.html',
]

# Old footer CSS patterns to remove
OLD_CSS_PATTERNS = [
    r'\.footer\{background:#111827;.*?\.footer-bottom-links a:hover\{color:white;\}',
    r'\.footer-grid-v2\{.*?@media\(max-width:640px\)\{\.footer-grid-v2\{.*?\}\}',
]

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)

    # 1. Inject new footer CSS (before </style>), avoid duplicates
    if 'FOOTER v2' not in html:
        # Remove old footer CSS blocks
        for pat in OLD_CSS_PATTERNS:
            html = re.sub(pat, '', html, flags=re.DOTALL)
        html = html.replace('</style>', NEW_FOOTER_CSS + '\n</style>', 1)

    # 2. Replace footer HTML (from <footer class="footer"> to </footer>)
    html = re.sub(
        r'<footer class="footer">.*?</footer>',
        NEW_FOOTER_HTML,
        html,
        flags=re.DOTALL,
        count=1
    )

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_footer.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
