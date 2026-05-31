#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guide design — Phase 3 : animations CSS + IntersectionObserver JS.

Injecte le bloc /* === ANIMATIONS VD v2 === */ + script scroll-reveal
sur tous les *.html. Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ANIM_CSS = """
/* === ANIMATIONS VD v2 === */
.btn-devis,.btn-primary,.sc-card-primary,.form-btn,.header-cta{
  transition:transform .3s ease,box-shadow .3s ease,background .2s ease;
}
.btn-devis:hover,.btn-primary:hover,.sc-card-primary:hover,.form-btn:hover,.header-cta:hover{
  transform:translateY(-2px);
  box-shadow:0 8px 24px rgba(0,155,116,.28);
}
.btn-devis:active,.btn-primary:active,.sc-card-primary:active,.form-btn:active{
  transform:scale(.98);
}
.btn-primary .arrow-icon,.other-card-cta .arrow-icon,.btn-devis .arrow-icon{
  transition:transform .3s ease;
}
.btn-primary:hover .arrow-icon,.other-card:hover .arrow-icon,
.btn-devis:hover .arrow-icon{transform:translateX(4px);}

.sc,.service-card,.other-card{
  transition:transform .35s ease,box-shadow .35s ease;
}
.sc:hover,.service-card:hover,.other-card:hover{
  transform:translateY(-8px);
  box-shadow:0 20px 40px rgba(0,0,0,.12);
}
.sc::before{
  content:'';position:absolute;inset:0;border-radius:inherit;
  background:linear-gradient(135deg,rgba(255,255,255,.12),transparent);
  opacity:0;transition:opacity .35s ease;pointer-events:none;
}
.sc:hover::before{opacity:.15;}

.sc-icon,.other-card-icon{
  transition:transform .35s ease;
}
.sc:hover .sc-icon,.other-card:hover .other-card-icon{
  transform:rotate(-5deg) scale(1.1);
}

.commune-pill{
  animation:vd-pill-in .45s ease both;
  transition:transform .25s ease,box-shadow .25s ease;
}
.commune-pill:nth-child(1){animation-delay:.03s;}
.commune-pill:nth-child(2){animation-delay:.06s;}
.commune-pill:nth-child(3){animation-delay:.09s;}
.commune-pill:nth-child(4){animation-delay:.12s;}
.commune-pill:nth-child(5){animation-delay:.15s;}
.commune-pill:nth-child(6){animation-delay:.18s;}
.commune-pill:nth-child(7){animation-delay:.21s;}
.commune-pill:nth-child(8){animation-delay:.24s;}
.commune-pill:nth-child(9){animation-delay:.27s;}
.commune-pill:nth-child(10){animation-delay:.30s;}
.commune-pill:nth-child(n+11){animation-delay:.33s;}
.commune-pill:hover{transform:scale(1.05);}

@keyframes vd-pill-in{
  from{opacity:0;transform:scale(.88);}
  to{opacity:1;transform:scale(1);}
}

.av-item,.enc-card,.av-list li{
  animation:vd-slide-in .5s ease both;
}
.av-list li:nth-child(1),.enc-card:nth-child(1){animation-delay:.05s;}
.av-list li:nth-child(2),.enc-card:nth-child(2){animation-delay:.1s;}
.av-list li:nth-child(3),.enc-card:nth-child(3){animation-delay:.15s;}
.av-list li:nth-child(4),.enc-card:nth-child(4){animation-delay:.2s;}
.av-list li:nth-child(5){animation-delay:.25s;}

@keyframes vd-slide-in{
  from{opacity:0;transform:translateY(16px);}
  to{opacity:1;transform:translateY(0);}
}

.animate-on-scroll{
  opacity:0;transform:translateY(24px);
  transition:opacity .4s ease,transform .4s ease;
}
.animate-on-scroll.animate-in{
  opacity:1;transform:translateY(0);
}

.sticky-mobile{
  transition:transform .35s cubic-bezier(.16,1,.3,1);
}

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{
    animation-duration:.01ms!important;
    animation-iteration-count:1!important;
    transition-duration:.01ms!important;
    scroll-behavior:auto!important;
  }
  .animate-on-scroll{opacity:1;transform:none;}
  .header-phone-pulse::after{display:none!important;}
}
"""

ANIM_JS = """
<script>
/* VD scroll animations v2 */
(function(){
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var els=document.querySelectorAll('.animate-on-scroll');
  if(!els.length)return;
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('animate-in');io.unobserve(e.target);}
    });
  },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  els.forEach(function(el){io.observe(el);});
})();
</script>"""

SCROLL_TARGETS = [
    ('class="services-grid"', 'class="services-grid animate-on-scroll"'),
    ('class="services-inner"', 'class="services-inner animate-on-scroll"'),
    ('class="encadres-grid"', 'class="encadres-grid animate-on-scroll"'),
    ('class="communes-cloud"', 'class="communes-cloud animate-on-scroll"'),
    ('class="other-grid"', 'class="other-grid animate-on-scroll"'),
    ('class="testimonials"', 'class="testimonials animate-on-scroll"'),
    ('class="cantons-inner"', 'class="cantons-inner animate-on-scroll"'),
]


def inject_css(html):
    if "ANIMATIONS VD v2" in html:
        return html
    return html.replace("</style>", ANIM_CSS + "\n</style>", 1)


def inject_js(html):
    if "VD scroll animations v2" in html:
        return html
    return html.replace("</body>", ANIM_JS + "\n</body>", 1)


def add_scroll_classes(html):
    for old, new in SCROLL_TARGETS:
        if "animate-on-scroll" in html and old.replace('class="', '') in html:
            pass
        html = html.replace(old, new)
    return html


def process(html):
    html = inject_css(html)
    html = add_scroll_classes(html)
    html = inject_js(html)
    return html


def main():
    changed = []
    for path in sorted(ROOT.glob("*.html")):
        orig = path.read_text(encoding="utf-8")
        new = process(orig)
        if new != orig:
            path.write_text(new, encoding="utf-8")
            changed.append(path.name)
    print(f"fix_animations_guide.py — {len(changed)} page(s) modifiée(s)")


if __name__ == "__main__":
    main()
