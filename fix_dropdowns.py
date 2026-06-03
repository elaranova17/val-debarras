#!/usr/bin/env python3
"""
Fix 1 — FAQ accordion fires twice (onclick + addEventListener clash)
Fix 2 — Navbar dropdown needs click JS (CSS-only hover unreliable)
Fix 3 — Add .nav-item.open .dd CSS so click-based open works
"""
import os, glob

PROTO = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

# ── Fix 1: Remove the redundant click addEventListener from FAQ JS ────────────
OLD_FAQ_LISTENERS = """  document.querySelectorAll('.faq-section .faq-q').forEach(function(btn){
    if(btn.dataset.faqBound) return;
    btn.dataset.faqBound = '1';
    if(!btn.hasAttribute('aria-expanded')) btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click', function(e){ e.preventDefault(); toggleFaq(btn); });
    btn.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); toggleFaq(btn); }
    });
  });"""

NEW_FAQ_LISTENERS = """  document.querySelectorAll('.faq-section .faq-q').forEach(function(btn){
    if(btn.dataset.faqBound) return;
    btn.dataset.faqBound = '1';
    if(!btn.hasAttribute('aria-expanded')) btn.setAttribute('aria-expanded','false');
    btn.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); toggleFaq(btn); }
    });
  });"""

# ── Fix 2+3: CSS + JS for nav dropdown click ─────────────────────────────────
# CSS to add right after `.nav-item:hover .dd{...}` rule
OLD_HOVER_RULE = '.nav-item:hover .dd{opacity:1;visibility:visible;transform:translateY(0);}'
NEW_HOVER_RULE = (
    '.nav-item:hover .dd{opacity:1;visibility:visible;transform:translateY(0);}\n'
    '.nav-item.open .dd{opacity:1;visibility:visible;transform:translateY(0);}'
)

# JS block to append before </body>
NAV_DROPDOWN_JS = """
<script>
/* Desktop nav dropdown — click toggle */
(function(){
  var navItems = document.querySelectorAll('#desktopNav .nav-item');
  if(!navItems.length) return;
  navItems.forEach(function(item){
    var btn = item.querySelector('.nav-btn');
    if(!btn) return;
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      var isOpen = item.classList.contains('open');
      navItems.forEach(function(i){ i.classList.remove('open'); });
      if(!isOpen) item.classList.add('open');
    });
  });
  document.addEventListener('click', function(){
    navItems.forEach(function(i){ i.classList.remove('open'); });
  });
})();
</script>
"""

files = glob.glob(os.path.join(PROTO, '*.html'))
f1 = f2css = f2js = 0

for path in sorted(files):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    # Fix 1 — FAQ double-fire
    if OLD_FAQ_LISTENERS in content:
        content = content.replace(OLD_FAQ_LISTENERS, NEW_FAQ_LISTENERS)
        f1 += 1

    # Fix 2 — nav dropdown CSS
    if OLD_HOVER_RULE in content and '.nav-item.open .dd' not in content:
        content = content.replace(OLD_HOVER_RULE, NEW_HOVER_RULE)
        f2css += 1

    # Fix 3 — nav dropdown JS (before </body>)
    if 'Desktop nav dropdown' not in content and '#desktopNav' in content:
        content = content.replace('</body>', NAV_DROPDOWN_JS + '</body>')
        f2js += 1

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  {os.path.basename(path)}')

print(f'\nFAQ fix: {f1} files | Nav CSS: {f2css} | Nav JS: {f2js}')
