#!/usr/bin/env python3
"""fix_cta_sticky.py
  1. Hero CTAs: téléphone grand (primaire) + devis + voir services
  2. Sticky bar mobile: 2 boutons fixes en bas, scroll-aware
"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'
FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
]

# ── CSS ───────────────────────────────────────────────────────────
NEW_CSS = """
/* ══════════════════════════════════════════════════
   HERO CTAs v2 — téléphone primaire + devis + services
   ══════════════════════════════════════════════════ */
.hero-btns{display:flex;gap:12px;flex-wrap:wrap;align-items:center;}

.btn-phone{
  display:inline-flex;align-items:center;gap:14px;
  background:white;color:var(--vert-fonce);
  padding:14px 24px;border-radius:14px;
  text-decoration:none;transition:all .22s;
  box-shadow:0 4px 16px rgba(0,0,0,.18);
  border:2px solid transparent;
}
.btn-phone:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.22);}
.btn-phone__icon{font-size:22px;flex-shrink:0;}
.btn-phone__text{display:flex;flex-direction:column;line-height:1.2;}
.btn-phone__num{font-size:18px;font-weight:900;letter-spacing:-.3px;}
.btn-phone__sub{font-size:11px;color:var(--vert);font-weight:600;opacity:.9;}

.btn-devis{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--vert);color:white;
  padding:14px 22px;border-radius:14px;
  font-weight:800;font-size:15px;
  text-decoration:none;transition:all .22s;
  border:2px solid transparent;
}
.btn-devis:hover{background:var(--vert-fonce);transform:translateY(-2px);}

.btn-services{
  display:inline-flex;align-items:center;gap:6px;
  background:transparent;color:rgba(255,255,255,.85);
  padding:14px 18px;border-radius:14px;
  font-weight:700;font-size:14px;
  text-decoration:none;transition:all .22s;
  border:2px solid rgba(255,255,255,.25);
}
.btn-services:hover{background:rgba(255,255,255,.1);color:white;border-color:rgba(255,255,255,.5);}

/* ══════════════════════════════════════════════════
   STICKY BAR MOBILE
   ══════════════════════════════════════════════════ */
.sticky-mobile{
  display:none;
  position:fixed;bottom:0;left:0;right:0;
  background:white;
  padding:12px 16px 16px;
  gap:10px;
  box-shadow:0 -4px 24px rgba(0,0,0,.15);
  z-index:800;
  transform:translateY(100%);
  transition:transform .35s cubic-bezier(.16,1,.3,1);
}
.sticky-mobile.visible{transform:translateY(0);}
.sticky-mobile__call{
  flex:1;background:var(--vert);color:white;
  padding:15px 12px;border-radius:10px;
  text-align:center;text-decoration:none;
  font-weight:800;font-size:16px;
  display:flex;align-items:center;justify-content:center;gap:8px;
}
.sticky-mobile__devis{
  flex:1;background:var(--gris-fonce);color:white;
  padding:15px 12px;border-radius:10px;
  text-align:center;text-decoration:none;
  font-weight:700;font-size:15px;
  display:flex;align-items:center;justify-content:center;gap:6px;
}
@media(max-width:768px){
  .sticky-mobile{display:flex;}
  /* Dar espacio al footer para que no tape contenido */
  body{padding-bottom:80px;}
}
"""

# ── HERO HTML: nuevos CTAs ────────────────────────────────────────
OLD_HERO_BTNS = '      <div class="hero-btns">\n        <a href="tel:0795805857" class="btn btn-white">📞 079 580 58 57</a>\n        <a href="#services" class="btn btn-outline">Voir nos services</a>\n      </div>'

NEW_HERO_BTNS = '''      <div class="hero-btns">
        <!-- CTA 1: Téléphone — primaire -->
        <a href="tel:+41795805857" class="btn-phone">
          <span class="btn-phone__icon">📞</span>
          <span class="btn-phone__text">
            <span class="btn-phone__num">079 580 58 57</span>
            <span class="btn-phone__sub">Appel gratuit · Lun–Sam 8h–18h</span>
          </span>
        </a>
        <!-- CTA 2: Devis -->
        <a href="#devis" class="btn-devis">📋 Devis gratuit</a>
        <!-- CTA 3: Services -->
        <a href="#services" class="btn-services">Nos services →</a>
      </div>'''

# ── STICKY BAR HTML ───────────────────────────────────────────────
STICKY_HTML = '''
<!-- ============================================================ -->
<!-- STICKY BAR MOBILE                                            -->
<!-- ============================================================ -->
<div class="sticky-mobile" id="stickyBar">
  <a href="tel:+41795805857" class="sticky-mobile__call">📞 Appeler</a>
  <a href="#devis" class="sticky-mobile__devis">📋 Devis gratuit</a>
</div>
'''

# ── STICKY JS ─────────────────────────────────────────────────────
STICKY_JS = '''
<script>
// Sticky bar mobile — scroll-aware
(function(){
  var bar = document.getElementById('stickyBar');
  if(!bar) return;
  var lastScroll = 0;
  // Aparece después de 3 segundos
  setTimeout(function(){ bar.classList.add('visible'); }, 3000);
  window.addEventListener('scroll', function(){
    var cur = window.pageYOffset;
    if(cur > lastScroll && cur > 200){
      bar.classList.remove('visible'); // bajando → ocultar
    } else {
      bar.classList.add('visible');    // subiendo → mostrar
    }
    lastScroll = cur;
  }, {passive:true});
})();
</script>'''

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)
    changes = []

    # 1. CSS
    if 'HERO CTAs v2' not in html:
        html = html.replace('</style>', NEW_CSS + '\n</style>', 1)
        changes.append('CSS')

    # 2. Hero CTAs (solo index.html tiene los btns exactos)
    if OLD_HERO_BTNS in html:
        html = html.replace(OLD_HERO_BTNS, NEW_HERO_BTNS, 1)
        changes.append('hero CTAs')

    # 3. Sticky bar HTML (antes de </body>)
    if 'stickyBar' not in html:
        html = html.replace('</body>', STICKY_HTML + STICKY_JS + '\n</body>', 1)
        changes.append('sticky bar')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

print('=== fix_cta_sticky.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
