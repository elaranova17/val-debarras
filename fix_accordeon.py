#!/usr/bin/env python3
"""fix_accordeon.py — Ronda 2:
  1. Service cards con acordeón expandible + CTA pre-selección formulario
  2. Tooltips en stats "+10 ans" y "500+"
"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

# ── CSS ───────────────────────────────────────────────────────────
NEW_CSS = """
/* ══════════════════════════════════════════════════
   SERVICE CARDS — acordeón expandible
   ══════════════════════════════════════════════════ */
.sc-toggle{
  background:none;border:none;cursor:pointer;font-family:var(--font);
  display:inline-flex;align-items:center;gap:7px;
  font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;
  color:rgba(255,255,255,.6);margin-top:22px;transition:all .2s;
  padding:0;
}
.sc-toggle:hover{color:white;}
.sc-arrow{display:inline-block;transition:transform .25s;font-style:normal;}
.sc.open .sc-arrow{transform:rotate(90deg);}

.sc-expanded{
  display:none;
  padding-top:14px;
  border-top:1px solid rgba(255,255,255,.12);
  margin-top:14px;
  animation:fadeSlideIn .28s ease;
}
.sc.open .sc-expanded{display:block;}
@keyframes fadeSlideIn{
  from{opacity:0;transform:translateY(-6px);}
  to{opacity:1;transform:translateY(0);}
}
.sc-features{
  list-style:none;display:flex;flex-direction:column;
  gap:8px;margin-bottom:14px;
}
.sc-features li{
  font-size:14px;color:rgba(255,255,255,.85);
  display:flex;align-items:flex-start;gap:8px;line-height:1.4;
}
.sc-features li span{color:#4ade80;font-weight:800;flex-shrink:0;}
.sc-cta-devis{
  display:flex;align-items:center;justify-content:center;gap:8px;
  background:white;color:var(--vert-fonce);
  padding:12px 16px;border-radius:10px;
  font-weight:800;font-size:13px;
  text-decoration:none;transition:all .2s;width:100%;
  box-sizing:border-box;
}
.sc-cta-devis:hover{background:var(--vert-clair);transform:translateY(-1px);}

/* ══════════════════════════════════════════════════
   STATS — tooltips au hover
   ══════════════════════════════════════════════════ */
.stat{position:relative;}
.stat[data-tip]:hover::after{
  content:attr(data-tip);
  position:absolute;bottom:calc(100% + 10px);left:50%;
  transform:translateX(-50%);
  background:rgba(15,23,42,.95);color:white;
  font-size:12px;font-weight:500;line-height:1.4;
  padding:8px 14px;border-radius:8px;
  white-space:nowrap;pointer-events:none;z-index:200;
  box-shadow:0 4px 16px rgba(0,0,0,.35);
}
.stat[data-tip]:hover::before{
  content:'';
  position:absolute;bottom:calc(100% + 4px);left:50%;
  transform:translateX(-50%);
  border:6px solid transparent;
  border-top-color:rgba(15,23,42,.95);
  pointer-events:none;z-index:200;
}
"""

# ── Services grid HTML (reemplaza todo el bloque) ─────────────────
SERVICES_DATA = [
    {
        'icon':'🏢','num':'01',
        'title':'Débarras appartement',
        'desc':'Votre appartement est trop encombré pour rendre les clés ? Nous vidons tout en 1 jour. Aucun tri demandé.',
        'href':'/debarras-appartement/',
        'service_select':'Débarras appartement',
        'features':['Aucun tri demandé de votre part','Vidage complet en 1 journée','Devis gratuit sous 24h'],
    },
    {
        'icon':'🏡','num':'02',
        'title':'Débarras maison',
        'desc':"Garage, grenier, jardin, cave — on s'occupe de tout. Même les gros volumes. En 1 jour.",
        'href':'/debarras-maison/',
        'service_select':'Débarras maison',
        'features':['Garage, grenier, cave inclus','Gros volumes acceptés','Intervention toute la Suisse romande'],
    },
    {
        'icon':'🕊️','num':'03',
        'title':'Débarras après décès/succession',
        'desc':'Un proche est décédé et vous devez vider son logement. Vous n\'avez pas à le faire seul.',
        'href':'/debarras-apres-deces/',
        'service_select':'Débarras après décès & succession',
        'features':['Discrétion et respect garantis','Coordination avec notaire possible','Remise des clés immédiate'],
    },
    {
        'icon':'🏥','num':'04',
        'title':'Débarras suite entrée EMS',
        'desc':'Votre parent entre en EMS ou en appartement protégé et il faut libérer le logement rapidement.',
        'href':'/debarras-ems/',
        'service_select':'Débarras suite entrée en EMS',
        'features':['Délais courts respectés','Tri et don aux associations','Logement prêt à rendre'],
    },
    {
        'icon':'⚠️','num':'05',
        'title':'Débarras Insalubre/Diogène',
        'desc':'Logement encombré, accumulation extrême, insalubrité. Nous intervenons sans jugement.',
        'href':'/debarras-insalubre-diogene/',
        'service_select':'Débarras insalubre / Diogène',
        'features':['Sans jugement, en toute discrétion','Équipe spécialisée et formée','Désinfection si nécessaire'],
    },
    {
        'icon':'🧹','num':'06',
        'title':'Nettoyages extrême',
        'desc':'Décès non découvert, contamination biologique, scène de crime. Protocole spécialisé. Discrétion absolue.',
        'href':'/nettoyage-extreme/',
        'service_select':'Nettoyages extrême',
        'features':['Protocole certifié biologique','Discrétion absolue garantie','Intervention sous 48h'],
    },
]

def make_card(s):
    features = '\n'.join(
        f'          <li><span>✓</span> {f}</li>' for f in s['features']
    )
    return f'''      <div class="sc" data-service="{s['service_select']}">
        <span class="sc-icon">{s['icon']}</span>
        <span class="sc-num">{s['num']}</span>
        <div>
          <div class="sc-title">{s['title']}</div>
          <p class="sc-desc">{s['desc']}</p>
        </div>
        <button class="sc-toggle" aria-expanded="false">
          Voir le service <i class="sc-arrow">→</i>
        </button>
        <div class="sc-expanded">
          <ul class="sc-features">
{features}
          </ul>
          <a href="#devis" class="sc-cta-devis" data-select="{s['service_select']}">
            📋 Devis gratuit — {s['title']} →
          </a>
        </div>
      </div>'''

NEW_GRID = '    <div class="services-grid">\n' + '\n'.join(make_card(s) for s in SERVICES_DATA) + '\n    </div>'

# ── JS acordeón + pre-selección formulario ────────────────────────
ACCORDION_JS = """
<script>
// ── Acordeón servicios ─────────────────────────────────────────
(function(){
  document.querySelectorAll('.sc-toggle').forEach(function(btn){
    btn.addEventListener('click', function(){
      var card = this.closest('.sc');
      var isOpen = card.classList.contains('open');
      document.querySelectorAll('.sc.open').forEach(function(c){
        c.classList.remove('open');
        c.querySelector('.sc-toggle').setAttribute('aria-expanded','false');
      });
      if(!isOpen){
        card.classList.add('open');
        this.setAttribute('aria-expanded','true');
      }
    });
  });

  // Pre-seleccionar servicio en el formulario
  document.querySelectorAll('.sc-cta-devis[data-select]').forEach(function(link){
    link.addEventListener('click', function(){
      var service = this.dataset.select;
      var sel = document.querySelector('#devis select, form select');
      if(sel){
        for(var i=0;i<sel.options.length;i++){
          if(sel.options[i].text.trim() === service){
            sel.selectedIndex = i; break;
          }
        }
      }
    });
  });
})();
</script>"""

# ── Stats tooltips: añadir data-tip a los dos primeros stats ──────
OLD_STAT_10 = '    <div class="stat">\n      <div class="stat-n">+10</div>\n      <div class="stat-l">ans d\'expérience</div>\n    </div>'
NEW_STAT_10 = '    <div class="stat" data-tip="Depuis 2015, plus de 3 500 interventions en Suisse romande">\n      <div class="stat-n">+10</div>\n      <div class="stat-l">ans d\'expérience</div>\n    </div>'

OLD_STAT_500 = '    <div class="stat">\n      <div class="stat-n">500+</div>\n      <div class="stat-l">logements vidés / an</div>\n    </div>'
NEW_STAT_500 = '    <div class="stat" data-tip="En moyenne 10 débarras par semaine, toute l\'année">\n      <div class="stat-n">500+</div>\n      <div class="stat-l">logements vidés / an</div>\n    </div>'

FILES = ['index.html']  # solo index tiene services-grid y stats

def patch(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    fname = os.path.basename(path)
    changes = []

    # 1. CSS
    if 'SERVICE CARDS — acordeón' not in html:
        html = html.replace('</style>', NEW_CSS + '\n</style>', 1)
        changes.append('CSS')

    # 2. Reemplazar services-grid completo
    new_html = re.sub(
        r'<div class="services-grid">.*?</div>\s*</div>\s*</section>',
        NEW_GRID + '\n    </div>\n</section>',
        html, count=1, flags=re.DOTALL
    )
    if new_html != html:
        html = new_html
        changes.append('services grid')

    # 3. Stats tooltips
    if OLD_STAT_10 in html:
        html = html.replace(OLD_STAT_10, NEW_STAT_10, 1)
        changes.append('stat +10 tip')
    if OLD_STAT_500 in html:
        html = html.replace(OLD_STAT_500, NEW_STAT_500, 1)
        changes.append('stat 500 tip')

    # 4. JS acordeón (antes de </body>)
    if 'Acordeón servicios' not in html:
        html = html.replace('</body>', ACCORDION_JS + '\n</body>', 1)
        changes.append('JS')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓ {fname}: {", ".join(changes)}')
    else:
        print(f'  ~ {fname}: no change')

# ── FAQ accordion + pro-section spacing (all service pages) ─────────
FAQ_JS_MARKER = '/* FAQ accordion — Val-Débarras */'
FAQ_JS = """
<script>
/* FAQ accordion — Val-Débarras */
(function(){
  if(window.__vdFaqInit) return;
  window.__vdFaqInit = true;

  function toggleFaq(btn){
    if(!btn) return;
    var answer = btn.nextElementSibling;
    if(!answer || !answer.classList.contains('faq-a')) return;
    var section = btn.closest('.faq-section');
    var isOpen = answer.classList.contains('open');

    if(section){
      section.querySelectorAll('.faq-a.open').forEach(function(a){
        if(a !== answer){
          a.classList.remove('open');
          var q = a.previousElementSibling;
          if(q && q.classList.contains('faq-q')) q.setAttribute('aria-expanded','false');
        }
      });
    }

    if(isOpen){
      answer.classList.remove('open');
      btn.setAttribute('aria-expanded','false');
    } else {
      answer.classList.add('open');
      btn.setAttribute('aria-expanded','true');
    }
  }
  window.toggleFaq = toggleFaq;

  document.querySelectorAll('.faq-section .faq-q').forEach(function(btn){
    if(btn.dataset.faqBound) return;
    btn.dataset.faqBound = '1';
    if(!btn.hasAttribute('aria-expanded')) btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click', function(e){ e.preventDefault(); toggleFaq(btn); });
    btn.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); toggleFaq(btn); }
    });
  });
})();
</script>"""

OLD_FAQ_ARR = '.faq-arr{font-size:12px;color:var(--vert);transition:transform .2s;flex-shrink:0;}'
NEW_FAQ_ARR = OLD_FAQ_ARR + '\n.faq-q[aria-expanded="true"] .faq-arr{transform:rotate(180deg);}'

OLD_PRO_SECTION = '.pro-section{max-width:860px;margin:0 auto 64px;padding:0 24px;}'
NEW_PRO_SECTION = '.pro-section{max-width:860px;margin:56px auto 64px;padding:0 24px;}'


def patch_faq_pages():
    html_files = [
        f for f in os.listdir(BASE)
        if f.endswith('.html') and os.path.isfile(os.path.join(BASE, f))
    ]
    for fname in sorted(html_files):
        path = os.path.join(BASE, fname)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        if '.faq-section' not in html and '<section class="pro-section">' not in html:
            continue
        original = html
        changes = []

        if OLD_FAQ_ARR in html and NEW_FAQ_ARR not in html:
            html = html.replace(OLD_FAQ_ARR, NEW_FAQ_ARR, 1)
            changes.append('faq chevron CSS')

        if '<section class="pro-section">' in html:
            if OLD_PRO_SECTION in html:
                html = html.replace(OLD_PRO_SECTION, NEW_PRO_SECTION, 1)
                changes.append('pro-section spacing')
            elif 'margin:56px auto 64px' not in html and '.pro-section{' in html:
                html = re.sub(
                    r'\.pro-section\{([^}]*?)margin:0 auto 64px',
                    r'.pro-section{\1margin:56px auto 64px',
                    html,
                    count=1,
                )
                if html != original:
                    changes.append('pro-section spacing (regex)')

        if '.faq-section' in html and FAQ_JS_MARKER not in html:
            html = html.replace('</body>', FAQ_JS + '\n</body>', 1)
            changes.append('FAQ JS')

        if html != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  ✓ {fname}: {", ".join(changes)}')
        else:
            print(f'  ~ {fname}: no change')


print('=== fix_accordeon.py ===')
patch(os.path.join(BASE, 'index.html'))
print('--- FAQ + pro-section ---')
patch_faq_pages()
print('Done.')
