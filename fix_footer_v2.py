#!/usr/bin/env python3
"""fix_footer_v2.py — Footer minimal: contacto izquierda + mapa Google Maps derecha"""
import re, os

BASE = '/Users/evelynpatino/Documents/Claude/Projects/Val-Debarras/prototype'

NEW_FOOTER = """<footer style="background-color:#1a1f2e;color:#fff;padding:60px 0;font-family:var(--font,system-ui,sans-serif);">
  <div style="max-width:1200px;margin:0 auto;padding:0 24px;display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start;">

    <!-- Contact -->
    <div>
      <h3 style="color:#4ade80;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:24px;">Contact</h3>

      <a href="tel:+41795805857" style="display:inline-flex;align-items:center;gap:12px;background:#2e7d5c;color:#fff;text-decoration:none;padding:14px 24px;border-radius:10px;font-size:18px;font-weight:700;margin-bottom:24px;transition:background .2s;" onmouseover="this.style.background='#1c5440'" onmouseout="this.style.background='#2e7d5c'">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        079 580 58 57
      </a>

      <div style="display:flex;flex-direction:column;gap:14px;color:#94a3b8;font-size:15px;line-height:1.6;">
        <div style="display:flex;align-items:center;gap:10px;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          <a href="mailto:info@val-debarras.ch" style="color:#94a3b8;text-decoration:none;">info@val-debarras.ch</a>
        </div>
        <div style="display:flex;align-items:flex-start;gap:10px;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" style="flex-shrink:0;margin-top:2px;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          <div>Rue de Mazerette 9<br>1950 Sion · Valais</div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>
          Lun–Sam · 08h00–18h00
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          Devis gratuit · Réponse sous 24h
        </div>
      </div>
    </div>

    <!-- Mapa -->
    <div style="width:100%;height:300px;border-radius:14px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.4);">
      <iframe
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2759.2!2d7.3524!3d46.2282!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x478ec04c47de8e2b%3A0x7c01a5b4b4a8b4e0!2sRue%20de%20Mazerette%209%2C%201950%20Sion!5e0!3m2!1sfr!2sch!4v1716900000000!5m2!1sfr!2sch"
        width="100%" height="100%"
        style="border:0;filter:grayscale(25%) contrast(1.1);"
        allowfullscreen="" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade">
      </iframe>
    </div>

  </div>

  <!-- Barre inférieure -->
  <div style="max-width:1200px;margin:40px auto 0;padding:24px 24px 0;border-top:1px solid #2d3748;display:flex;justify-content:space-between;align-items:center;color:#64748b;font-size:13px;flex-wrap:wrap;gap:12px;">
    <div>© 2026 Val-Débarras Sàrl — Tous droits réservés</div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;">
      <a href="#" style="color:#64748b;text-decoration:none;">Protection des données</a>
      <a href="#" style="color:#64748b;text-decoration:none;">Conditions générales</a>
      <a href="/brand" style="color:#2e7d5c;text-decoration:none;font-weight:600;">🎨 Charte</a>
    </div>
  </div>
</footer>"""

FILES = [
    'index.html',
    'ge-appartement.html','ge-maison.html','ge-succession.html',
    'ge-ems.html','ge-diogene.html','ge-nettoyage.html',
    'blog.html','blog-article-1.html',
]

def patch(path):
    with open(path,'r',encoding='utf-8') as f:
        html = f.read()
    new_html = re.sub(r'<footer[\s\S]*?</footer>', NEW_FOOTER, html, count=1)
    if new_html != html:
        with open(path,'w',encoding='utf-8') as f:
            f.write(new_html)
        print(f'  ✓ {os.path.basename(path)}')
    else:
        print(f'  ~ {os.path.basename(path)}: no footer found')

print('=== fix_footer_v2.py ===')
for fname in FILES:
    patch(os.path.join(BASE, fname))
print('Done.')
