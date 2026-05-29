#!/usr/bin/env python3
"""fix_testimonios.py — Ronda 3:
  1. Sección testimonios (3 cards + carrusel mobile) — après cantons
  2. Botones A+/A- en header + modo lectura
"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

# ── CSS ───────────────────────────────────────────────────────────
NEW_CSS = """
/* ══════════════════════════════════════════════════
   TESTIMONIOS
   ══════════════════════════════════════════════════ */
.testimonials{background:#f8fafc;padding:80px 0;border-top:1px solid #eff0f2;}
.testimonials-inner{max-width:1200px;margin:0 auto;padding:0 24px;}
.testi-grid{
  display:grid;grid-template-columns:repeat(3,1fr);
  gap:24px;margin-top:48px;
}
.testi-card{
  background:white;border-radius:16px;padding:28px;
  box-shadow:0 2px 12px rgba(0,0,0,.06);
  border:1px solid #f0f0f0;
  display:flex;flex-direction:column;gap:16px;
  transition:box-shadow .2s;
}
.testi-card:hover{box-shadow:0 8px 28px rgba(0,0,0,.10);}
.testi-stars{color:#f59e0b;font-size:18px;letter-spacing:2px;}
.testi-quote{
  font-size:16px;color:#374151;line-height:1.7;
  font-style:italic;flex:1;
}
.testi-quote::before{content:'"';font-size:40px;color:var(--vert);line-height:0;vertical-align:-.4em;margin-right:4px;}
.testi-author{display:flex;align-items:center;gap:12px;padding-top:16px;border-top:1px solid #f3f4f6;}
.testi-avatar{
  width:48px;height:48px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-weight:900;font-size:16px;color:white;flex-shrink:0;
}
.testi-info{display:flex;flex-direction:column;gap:2px;}
.testi-name{font-size:15px;font-weight:700;color:#1f2937;}
.testi-location{font-size:13px;color:#6b7280;}
.testi-service{
  display:inline-block;font-size:11px;font-weight:700;
  color:var(--vert);background:var(--vert-clair);
  padding:2px 8px;border-radius:20px;margin-top:2px;
}
/* Mobile: scroll horizontal */
@media(max-width:768px){
  .testi-grid{
    grid-template-columns:repeat(3,85vw);
    overflow-x:auto;scroll-snap-type:x mandatory;
    padding-bottom:12px;gap:16px;
    -webkit-overflow-scrolling:touch;
  }
  .testi-card{scroll-snap-align:center;}
}

/* ══════════════════════════════════════════════════
   A+ / A- — Contrôle taille texte
   ══════════════════════════════════════════════════ */
.a11y-size{
  display:flex;align-items:center;gap:4px;
  flex-shrink:0;margin-left:8px;
}
.a-btn{
  background:#f3f4f6;border:1px solid #e5e7eb;
  border-radius:6px;cursor:pointer;
  font-family:var(--font);font-weight:800;color:#374151;
  padding:5px 9px;font-size:13px;
  transition:all .15s;line-height:1;
}
.a-btn:hover{background:var(--vert-clair);border-color:var(--vert);color:var(--vert-fonce);}
.a-btn:active{transform:scale(.95);}
@media(max-width:768px){.a11y-size{display:none;}}

/* Modo lectura */
body.mode-lecture{
  background:#faf8f4 !important;
  font-size:20px !important;
  line-height:1.8 !important;
}
body.mode-lecture .hero::after,
body.mode-lecture .services,
body.mode-lecture .video-dark{opacity:.92;}
.mode-btn{
  display:flex;align-items:center;gap:5px;
  background:#f3f4f6;border:1px solid #e5e7eb;
  border-radius:6px;cursor:pointer;
  font-family:var(--font);font-weight:700;color:#374151;
  padding:5px 10px;font-size:12px;white-space:nowrap;
  transition:all .15s;
}
.mode-btn:hover{background:var(--vert-clair);border-color:var(--vert);color:var(--vert-fonce);}
.mode-btn.active{background:var(--vert);color:white;border-color:var(--vert-fonce);}
@media(max-width:1024px){.mode-btn{display:none;}}
"""

# ── Testimonios HTML ──────────────────────────────────────────────
TESTIMONIOS_HTML = """
<!-- ============================================================ -->
<!-- TESTIMONIOS                                                   -->
<!-- ============================================================ -->
<section class="testimonials">
  <div class="testimonials-inner">
    <div class="section-top">
      <span class="section-kicker">Avis clients vérifiés</span>
      <h2 class="section-h2">Ils nous font confiance</h2>
      <p class="section-p">Plus de 500 interventions par année dans toute la Suisse romande.</p>
    </div>
    <div class="testi-grid">

      <div class="testi-card">
        <div class="testi-stars">⭐⭐⭐⭐⭐</div>
        <p class="testi-quote">Intervention rapide et discrète après le décès de ma mère. L'équipe a été d'un grand respect et professionnalisme dans un moment très difficile.</p>
        <div class="testi-author">
          <div class="testi-avatar" style="background:#2e7d5c;">MD</div>
          <div class="testi-info">
            <span class="testi-name">Marie D.</span>
            <span class="testi-location">Lausanne · Vaud</span>
            <span class="testi-service">Après décès / succession</span>
          </div>
        </div>
      </div>

      <div class="testi-card">
        <div class="testi-stars">⭐⭐⭐⭐⭐</div>
        <p class="testi-quote">Appartement de 4 pièces vidé en une seule journée. Devis honnête, équipe ponctuelle, aucun tri demandé de notre part. Je recommande sans hésiter.</p>
        <div class="testi-author">
          <div class="testi-avatar" style="background:#1c5440;">PM</div>
          <div class="testi-info">
            <span class="testi-name">Pierre &amp; Anne M.</span>
            <span class="testi-location">Genève · GE</span>
            <span class="testi-service">Débarras appartement</span>
          </div>
        </div>
      </div>

      <div class="testi-card">
        <div class="testi-stars">⭐⭐⭐⭐⭐</div>
        <p class="testi-quote">Mon père entrait en EMS et il fallait libérer son appartement en 10 jours. Val-Débarras a tout géré, même les meubles à donner à la Croix-Rouge.</p>
        <div class="testi-author">
          <div class="testi-avatar" style="background:#163d28;">JF</div>
          <div class="testi-info">
            <span class="testi-name">Jean-Claude F.</span>
            <span class="testi-location">Sion · Valais</span>
            <span class="testi-service">Suite entrée EMS</span>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>
"""

# ── A+/A-/Mode lecture en header HTML ────────────────────────────
OLD_HEADER_CTA = '    <a href="tel:0795805857" class="header-cta">📞 079 580 58 57</a>'
NEW_HEADER_CTA = '''    <div class="a11y-size">
      <button class="a-btn" id="aMinus" aria-label="Réduire le texte" title="Texte plus petit">A−</button>
      <button class="a-btn" id="aPlus" aria-label="Agrandir le texte" title="Texte plus grand">A+</button>
      <button class="mode-btn" id="modeLecture" aria-label="Mode lecture simplifiée">📖 Lecture</button>
    </div>
    <a href="tel:0795805857" class="header-cta">📞 079 580 58 57</a>'''

# ── JS ────────────────────────────────────────────────────────────
A11Y_JS = """
<script>
// ── A+ / A- taille du texte ────────────────────────────────────
(function(){
  var sizes = [15, 16, 18, 20];
  var idx = 1; // 16px par défaut
  var root = document.documentElement;

  var aPlus = document.getElementById('aPlus');
  var aMinus = document.getElementById('aMinus');
  var modeBtn = document.getElementById('modeLecture');

  if(aPlus) aPlus.addEventListener('click', function(){
    if(idx < sizes.length-1){ idx++; root.style.fontSize = sizes[idx]+'px'; }
  });
  if(aMinus) aMinus.addEventListener('click', function(){
    if(idx > 0){ idx--; root.style.fontSize = sizes[idx]+'px'; }
  });

  // Mode lecture
  if(modeBtn) modeBtn.addEventListener('click', function(){
    document.body.classList.toggle('mode-lecture');
    this.classList.toggle('active');
    this.textContent = document.body.classList.contains('mode-lecture')
      ? '✕ Normal' : '📖 Lecture';
  });
})();
</script>"""

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)
    changes = []

    # 1. CSS
    if 'TESTIMONIOS' not in html:
        html = html.replace('</style>', NEW_CSS + '\n</style>', 1)
        changes.append('CSS')

    # 2. Testimonios: insertar antes de <!-- BLOG PREVIEW -->
    if 'class="testi-grid"' not in html and '<!-- BLOG PREVIEW' in html:
        html = html.replace('<!-- BLOG PREVIEW — Phase 4.6', TESTIMONIOS_HTML + '\n<!-- BLOG PREVIEW — Phase 4.6', 1)
        changes.append('testimonios')

    # 3. A+/A- en header
    if 'id="aPlus"' not in html and OLD_HEADER_CTA in html:
        html = html.replace(OLD_HEADER_CTA, NEW_HEADER_CTA, 1)
        changes.append('A+/A-')

    # 4. JS
    if 'A+ / A-' not in html:
        html = html.replace('</body>', A11Y_JS + '\n</body>', 1)
        changes.append('JS')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
]

print('=== fix_testimonios.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
