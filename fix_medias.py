#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reorganiza la sección de medios del home (index.html):
- Elimina la banda de badges repetidos ("Plus de 10 ans... Passés dans les médias")
- Reemplaza la sección video-dark (tabs RTS/20min) por 2 tarjetas independientes y coherentes
- Inyecta el CSS de las tarjetas
- Elimina el JS de los tabs (ya no se usa)

Tarjetas = enlaces directos (abren el reportaje/artículo en nueva pestaña),
fiable porque RTS/20min bloquean el embebido en iframe.
Idempotente.
"""
import re
from pathlib import Path

BASE = Path(__file__).parent
PAGE = BASE / "index.html"

NEW_SECTION = '''<section class="media-section" id="medias">
  <div class="media-container">

    <div class="media-header">
      <span class="section-label">Ils parlent de nous</span>
      <h2 class="section-title">Passés dans les médias suisses</h2>
      <p class="section-desc">Cliquez sur chaque média pour voir le reportage ou lire l'article</p>
    </div>

    <div class="media-grid">

      <!-- TARJETA 1: RTS (VIDEO) -->
      <a class="media-card media-card-video"
         href="https://www.rts.ch/play/tv/temps-present/video/diogenes-une-montagne-de-souffrance?urn=urn:rts:video:8430900a-7072-3ba2-aacb-9a1268ffceef"
         target="_blank" rel="noopener noreferrer"
         aria-label="Voir le reportage RTS - Temps Présent: Diogène, une montagne de souffrance. Durée 29 minutes 48.">
        <div class="media-preview">
          <img src="/images/rts-preview.jpg" onerror="this.src='/images/ge-action.jpg'"
               alt="Camion Val-Débarras devant un logement insalubre. Reportage RTS sur le syndrome de Diogène en Suisse romande."
               class="media-preview-img" loading="lazy">
          <span class="media-badge media-badge-rts">RTS</span>
          <div class="media-play-btn" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="12" fill="#009b74"/>
              <path d="M10 8L16 12L10 16V8Z" fill="white"/>
            </svg>
          </div>
          <span class="media-duration">29:48</span>
        </div>
        <div class="media-info">
          <h3 class="media-title">Temps Présent — RTS</h3>
          <p class="media-subtitle">Diogène : une montagne de souffrance</p>
          <span class="media-type">Reportage vidéo · 29:48</span>
        </div>
      </a>

      <!-- TARJETA 2: 20 MINUTES (ARTICLE) -->
      <a class="media-card media-card-article"
         href="https://www.20min.ch/fr/story/valais-locataire-expulsee-elle-conservait-35-tonnes-de-dechets-103216100"
         target="_blank" rel="noopener noreferrer"
         aria-label="Lire l'article 20 Minutes: Locataire expulsée à Sion, elle conservait 3,5 tonnes de déchets.">
        <div class="media-preview">
          <img src="/images/ge-action.jpg"
               alt="Appartement encombré avec des piles de déchets. Article 20 Minutes sur une locataire expulsée à Sion."
               class="media-preview-img" loading="lazy">
          <span class="media-badge media-badge-20min">20 minutes</span>
          <div class="media-article-icon" aria-hidden="true">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
              <path d="M4 4h16v16H4z"/>
              <path d="M8 8h8M8 12h8M8 16h5"/>
            </svg>
          </div>
        </div>
        <div class="media-info">
          <h3 class="media-title">20 Minutes Suisse</h3>
          <p class="media-subtitle">Valais : locataire expulsée, 35 tonnes de déchets</p>
          <span class="media-type">Article · 20 Minutes</span>
        </div>
      </a>

    </div>
  </div>
</section>'''

NEW_CSS = '''
/* ========== SECCIÓN MEDIOS (rediseñada) ========== */
.media-section{background:#0f172a;padding:80px 24px;}
.media-container{max-width:1000px;margin:0 auto;}
.media-header{margin-bottom:48px;text-align:center;}
.media-section .section-label{display:block;font-size:.9rem;font-weight:600;color:#009b74;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;}
.media-section .section-title{font-size:2rem;font-weight:700;color:#fff;margin-bottom:12px;}
.media-section .section-desc{font-size:1rem;color:#94a3b8;}
.media-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:32px;}
.media-card{background:#1e293b;border-radius:16px;overflow:hidden;cursor:pointer;transition:all .3s cubic-bezier(.4,0,.2,1);border:2px solid transparent;text-decoration:none;display:block;color:inherit;}
.media-card-video:hover{border-color:#e30613;transform:translateY(-6px);box-shadow:0 20px 40px rgba(227,6,19,.15);}
.media-card-article:hover{border-color:#0055ff;transform:translateY(-6px);box-shadow:0 20px 40px rgba(0,85,255,.15);}
.media-preview{position:relative;aspect-ratio:16/9;overflow:hidden;}
.media-preview-img{width:100%;height:100%;object-fit:cover;transition:transform .4s ease;}
.media-card:hover .media-preview-img{transform:scale(1.05);}
.media-badge{position:absolute;top:16px;left:16px;padding:6px 14px;border-radius:6px;font-size:.8rem;font-weight:700;color:#fff;z-index:2;}
.media-badge-rts{background:#e30613;}
.media-badge-20min{background:#0055ff;}
.media-play-btn{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:64px;height:64px;background:rgba(0,155,116,.9);border-radius:50%;display:flex;align-items:center;justify-content:center;transition:all .3s ease;z-index:2;}
.media-card:hover .media-play-btn{transform:translate(-50%,-50%) scale(1.1);background:#009b74;}
.media-duration{position:absolute;bottom:16px;right:16px;background:rgba(0,0,0,.8);color:#fff;padding:6px 10px;border-radius:4px;font-size:.8rem;font-weight:600;z-index:2;}
.media-article-icon{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:64px;height:64px;background:rgba(0,85,255,.9);border-radius:50%;display:flex;align-items:center;justify-content:center;transition:all .3s ease;z-index:2;opacity:0;}
.media-card-article:hover .media-article-icon{opacity:1;transform:translate(-50%,-50%) scale(1.1);}
.media-info{padding:24px;}
.media-title{font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:6px;}
.media-subtitle{font-size:.95rem;color:#94a3b8;margin-bottom:12px;line-height:1.4;}
.media-type{font-size:.8rem;color:#64748b;font-style:italic;}
@media(max-width:768px){.media-grid{grid-template-columns:1fr;}.media-section .section-title{font-size:1.5rem;}}
'''


def main():
    html = PAGE.read_text(encoding="utf-8")
    before = html

    # 1) Eliminar la banda de badges repetidos
    html = re.sub(
        r'<div class="medias">.*?</div>\s*</div>\s*</div>',
        '',
        html, count=1, flags=re.DOTALL,
    )

    # 2) Reemplazar la sección video-dark por las tarjetas
    html = re.sub(
        r'<section class="video-dark">.*?</section>',
        NEW_SECTION,
        html, count=1, flags=re.DOTALL,
    )

    # 3) Eliminar el JS de los tabs (ya sin uso)
    html = re.sub(
        r'<script>\s*/\* ── TABS MÉDIAS JS ── \*/.*?</script>',
        '',
        html, count=1, flags=re.DOTALL,
    )

    # 4) Inyectar CSS (idempotente)
    if '.media-section{' not in html:
        html = html.replace('</style>', NEW_CSS + '</style>', 1)

    if html != before:
        PAGE.write_text(html, encoding="utf-8")
        print("index.html actualizado.")
    else:
        print("Sin cambios (¿ya aplicado?).")


if __name__ == "__main__":
    main()
