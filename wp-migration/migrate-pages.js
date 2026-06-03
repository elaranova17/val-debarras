/**
 * Val-Débarras — Migración de contenido HTML → WordPress
 * Version 2 — incluye páginas merci (3 niveles de jerarquía)
 *
 * PREREQUISITOS:
 *  1. WPCode snippet "VD Full Page Renderer" instalado y ACTIVO
 *     (registra _vd_html en la REST API y sirve HTML directo)
 *  2. Correr en el console del navegador estando en:
 *     https://www.val-debarras.ch/wp-admin/
 *  3. Reemplazar VERCEL_BASE_URL con la URL real del deploy en Vercel
 *
 * INSTRUCCIONES:
 *  - Ir a https://www.val-debarras.ch/wp-admin/
 *  - DevTools → Console → pegar todo este script → Enter
 *  - El progreso aparece en la consola (✅ ok, ❌ error, ⚠️ skip)
 */

(async function vdMigrate() {
  'use strict';

  // ╔══════════════════════════════════════════════════════════════════╗
  // ║  CONFIGURACIÓN — AJUSTAR ANTES DE CORRER                        ║
  // ╚══════════════════════════════════════════════════════════════════╝

  // URL base de la preview Vercel (sin barra final)
  // Encontrar en: https://vercel.com/dashboard → proyecto val-debarras → Deployments
  const VERCEL_BASE_URL = 'https://val-debarras-prototype.vercel.app';

  // Delay entre requests (ms) — no bajar de 200
  const DELAY_MS = 300;

  // ╔══════════════════════════════════════════════════════════════════╗
  // ║  PÁGINAS A MIGRAR                                               ║
  // ╚══════════════════════════════════════════════════════════════════╝
  //
  //  { src: '/url-en-vercel', slug, parentSlug?, grandparentSlug? }
  //
  //  Jerarquía WP:
  //   - Nivel 1 (raíz)     : { slug, parentSlug: null }
  //   - Nivel 2 (canton)   : { slug, parentSlug: 'servicio' }
  //   - Nivel 3 (merci)    : { slug: 'merci', parentSlug: 'canton', grandparentSlug: 'servicio' }

  const PAGES = [

    // ── Home ──────────────────────────────────────────────────────────
    // Nota: La home WP (ID=2 o front page) normalmente tiene parent=0 y slug=''.
    // Si falla, ajustar manualmente vía WP Admin.
    // { src: '/', slug: '', parentSlug: null },  // Descomentar si es necesario

    // ── Merci genérica ────────────────────────────────────────────────
    { src: '/merci', slug: 'merci', parentSlug: null },

    // ── Páginas genéricas de servicio ─────────────────────────────────
    { src: '/debarras-appartement',           slug: 'debarras-appartement',           parentSlug: null },
    { src: '/debarras-maison',                slug: 'debarras-maison',                parentSlug: null },
    { src: '/debarras-apres-deces-succession',slug: 'debarras-apres-deces-succession',parentSlug: null },
    { src: '/debarras-ems',                   slug: 'debarras-ems',                   parentSlug: null },
    { src: '/debarras-insalubre-diogene',     slug: 'debarras-insalubre-diogene',     parentSlug: null },
    { src: '/nettoyage-extreme',              slug: 'nettoyage-extreme',              parentSlug: null },

    // ── Appartement × Cantons ─────────────────────────────────────────
    { src: '/debarras-appartement/geneve',    slug: 'geneve',    parentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/vaud',      slug: 'vaud',      parentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/valais',    slug: 'valais',    parentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/fribourg',  slug: 'fribourg',  parentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/neuchatel', slug: 'neuchatel', parentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/jura',      slug: 'jura',      parentSlug: 'debarras-appartement' },

    // ── Appartement × Merci ───────────────────────────────────────────
    { src: '/debarras-appartement/geneve/merci',    slug: 'merci', parentSlug: 'geneve',    grandparentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/vaud/merci',      slug: 'merci', parentSlug: 'vaud',      grandparentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/valais/merci',    slug: 'merci', parentSlug: 'valais',    grandparentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/fribourg/merci',  slug: 'merci', parentSlug: 'fribourg',  grandparentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/neuchatel/merci', slug: 'merci', parentSlug: 'neuchatel', grandparentSlug: 'debarras-appartement' },
    { src: '/debarras-appartement/jura/merci',      slug: 'merci', parentSlug: 'jura',      grandparentSlug: 'debarras-appartement' },

    // ── Maison × Cantons ──────────────────────────────────────────────
    { src: '/debarras-maison/geneve',    slug: 'geneve',    parentSlug: 'debarras-maison' },
    { src: '/debarras-maison/vaud',      slug: 'vaud',      parentSlug: 'debarras-maison' },
    { src: '/debarras-maison/valais',    slug: 'valais',    parentSlug: 'debarras-maison' },
    { src: '/debarras-maison/fribourg',  slug: 'fribourg',  parentSlug: 'debarras-maison' },
    { src: '/debarras-maison/neuchatel', slug: 'neuchatel', parentSlug: 'debarras-maison' },
    { src: '/debarras-maison/jura',      slug: 'jura',      parentSlug: 'debarras-maison' },

    // ── Maison × Merci ────────────────────────────────────────────────
    { src: '/debarras-maison/geneve/merci',    slug: 'merci', parentSlug: 'geneve',    grandparentSlug: 'debarras-maison' },
    { src: '/debarras-maison/vaud/merci',      slug: 'merci', parentSlug: 'vaud',      grandparentSlug: 'debarras-maison' },
    { src: '/debarras-maison/valais/merci',    slug: 'merci', parentSlug: 'valais',    grandparentSlug: 'debarras-maison' },
    { src: '/debarras-maison/fribourg/merci',  slug: 'merci', parentSlug: 'fribourg',  grandparentSlug: 'debarras-maison' },
    { src: '/debarras-maison/neuchatel/merci', slug: 'merci', parentSlug: 'neuchatel', grandparentSlug: 'debarras-maison' },
    { src: '/debarras-maison/jura/merci',      slug: 'merci', parentSlug: 'jura',      grandparentSlug: 'debarras-maison' },

    // ── Succession × Cantons ──────────────────────────────────────────
    { src: '/debarras-apres-deces-succession/geneve',    slug: 'geneve',    parentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/vaud',      slug: 'vaud',      parentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/valais',    slug: 'valais',    parentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/fribourg',  slug: 'fribourg',  parentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/neuchatel', slug: 'neuchatel', parentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/jura',      slug: 'jura',      parentSlug: 'debarras-apres-deces-succession' },

    // ── Succession × Merci ────────────────────────────────────────────
    { src: '/debarras-apres-deces-succession/geneve/merci',    slug: 'merci', parentSlug: 'geneve',    grandparentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/vaud/merci',      slug: 'merci', parentSlug: 'vaud',      grandparentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/valais/merci',    slug: 'merci', parentSlug: 'valais',    grandparentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/fribourg/merci',  slug: 'merci', parentSlug: 'fribourg',  grandparentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/neuchatel/merci', slug: 'merci', parentSlug: 'neuchatel', grandparentSlug: 'debarras-apres-deces-succession' },
    { src: '/debarras-apres-deces-succession/jura/merci',      slug: 'merci', parentSlug: 'jura',      grandparentSlug: 'debarras-apres-deces-succession' },

    // ── EMS × Cantons ─────────────────────────────────────────────────
    { src: '/debarras-ems/geneve',    slug: 'geneve',    parentSlug: 'debarras-ems' },
    { src: '/debarras-ems/vaud',      slug: 'vaud',      parentSlug: 'debarras-ems' },
    { src: '/debarras-ems/valais',    slug: 'valais',    parentSlug: 'debarras-ems' },
    { src: '/debarras-ems/fribourg',  slug: 'fribourg',  parentSlug: 'debarras-ems' },
    { src: '/debarras-ems/neuchatel', slug: 'neuchatel', parentSlug: 'debarras-ems' },
    { src: '/debarras-ems/jura',      slug: 'jura',      parentSlug: 'debarras-ems' },

    // ── EMS × Merci ───────────────────────────────────────────────────
    { src: '/debarras-ems/geneve/merci',    slug: 'merci', parentSlug: 'geneve',    grandparentSlug: 'debarras-ems' },
    { src: '/debarras-ems/vaud/merci',      slug: 'merci', parentSlug: 'vaud',      grandparentSlug: 'debarras-ems' },
    { src: '/debarras-ems/valais/merci',    slug: 'merci', parentSlug: 'valais',    grandparentSlug: 'debarras-ems' },
    { src: '/debarras-ems/fribourg/merci',  slug: 'merci', parentSlug: 'fribourg',  grandparentSlug: 'debarras-ems' },
    { src: '/debarras-ems/neuchatel/merci', slug: 'merci', parentSlug: 'neuchatel', grandparentSlug: 'debarras-ems' },
    { src: '/debarras-ems/jura/merci',      slug: 'merci', parentSlug: 'jura',      grandparentSlug: 'debarras-ems' },

    // ── Insalubre Diogène × Cantons ───────────────────────────────────
    { src: '/debarras-insalubre-diogene/geneve',    slug: 'geneve',    parentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/vaud',      slug: 'vaud',      parentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/valais',    slug: 'valais',    parentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/fribourg',  slug: 'fribourg',  parentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/neuchatel', slug: 'neuchatel', parentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/jura',      slug: 'jura',      parentSlug: 'debarras-insalubre-diogene' },

    // ── Insalubre × Merci ─────────────────────────────────────────────
    { src: '/debarras-insalubre-diogene/geneve/merci',    slug: 'merci', parentSlug: 'geneve',    grandparentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/vaud/merci',      slug: 'merci', parentSlug: 'vaud',      grandparentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/valais/merci',    slug: 'merci', parentSlug: 'valais',    grandparentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/fribourg/merci',  slug: 'merci', parentSlug: 'fribourg',  grandparentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/neuchatel/merci', slug: 'merci', parentSlug: 'neuchatel', grandparentSlug: 'debarras-insalubre-diogene' },
    { src: '/debarras-insalubre-diogene/jura/merci',      slug: 'merci', parentSlug: 'jura',      grandparentSlug: 'debarras-insalubre-diogene' },

    // ── Nettoyage Extrême × Cantons ───────────────────────────────────
    { src: '/nettoyage-extreme/geneve',    slug: 'geneve',    parentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/vaud',      slug: 'vaud',      parentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/valais',    slug: 'valais',    parentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/fribourg',  slug: 'fribourg',  parentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/neuchatel', slug: 'neuchatel', parentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/jura',      slug: 'jura',      parentSlug: 'nettoyage-extreme' },

    // ── Nettoyage × Merci ─────────────────────────────────────────────
    { src: '/nettoyage-extreme/geneve/merci',    slug: 'merci', parentSlug: 'geneve',    grandparentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/vaud/merci',      slug: 'merci', parentSlug: 'vaud',      grandparentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/valais/merci',    slug: 'merci', parentSlug: 'valais',    grandparentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/fribourg/merci',  slug: 'merci', parentSlug: 'fribourg',  grandparentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/neuchatel/merci', slug: 'merci', parentSlug: 'neuchatel', grandparentSlug: 'nettoyage-extreme' },
    { src: '/nettoyage-extreme/jura/merci',      slug: 'merci', parentSlug: 'jura',      grandparentSlug: 'nettoyage-extreme' },
  ];

  // ╔══════════════════════════════════════════════════════════════════╗
  // ║  HELPERS                                                        ║
  // ╚══════════════════════════════════════════════════════════════════╝

  const delay = ms => new Promise(r => setTimeout(r, ms));

  // Cache de IDs de páginas para evitar buscar el mismo padre N veces
  const _idCache = new Map();

  async function fetchPages(slug) {
    if (_idCache.has(slug)) return _idCache.get(slug);
    const res = await fetch(
      `/wp-json/wp/v2/pages?slug=${encodeURIComponent(slug)}&per_page=50`,
      { credentials: 'include' }
    );
    const data = await res.json();
    _idCache.set(slug, data);
    return data;
  }

  /**
   * Busca el ID de una página WP dado su slug y cadena de ancestros.
   * @param {string} slug
   * @param {string|null} parentSlug
   * @param {string|null} grandparentSlug
   * @returns {number|null}
   */
  async function getPageId(slug, parentSlug = null, grandparentSlug = null) {
    const pages = await fetchPages(slug);

    // Nivel 1: sin padre
    if (!parentSlug) {
      const found = pages.find(p => p.parent === 0);
      return found ? found.id : null;
    }

    // Resolver ID del padre
    const parentPages = await fetchPages(parentSlug);
    let parentId;

    if (!grandparentSlug) {
      // Padre es nivel 1
      const parentPage = parentPages.find(p => p.parent === 0);
      if (!parentPage) { console.warn(`⚠️  Padre raíz no encontrado: "${parentSlug}"`); return null; }
      parentId = parentPage.id;
    } else {
      // Padre es nivel 2: necesitamos el abuelo primero
      const grandParentPages = await fetchPages(grandparentSlug);
      const grandParent = grandParentPages.find(p => p.parent === 0);
      if (!grandParent) { console.warn(`⚠️  Abuelo no encontrado: "${grandparentSlug}"`); return null; }
      const parentPage = parentPages.find(p => p.parent === grandParent.id);
      if (!parentPage) { console.warn(`⚠️  Padre nivel-2 no encontrado: "${parentSlug}" bajo "${grandparentSlug}"`); return null; }
      parentId = parentPage.id;
    }

    const child = pages.find(p => p.parent === parentId);
    return child ? child.id : null;
  }

  /** Guarda el HTML en el meta _vd_html de una página WP */
  async function updatePageMeta(pageId, html) {
    const nonce = (typeof wpApiSettings !== 'undefined' && wpApiSettings.nonce)
      ? wpApiSettings.nonce
      : document.cookie.match(/wordpress_logged_in_[^=]+=([^;]+)/)?.[1] ?? '';

    const res = await fetch(`/wp-json/wp/v2/pages/${pageId}`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-WP-Nonce': nonce,
      },
      body: JSON.stringify({ meta: { _vd_html: html } }),
    });

    const txt = await res.text();
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${txt.slice(0, 300)}`);
    return JSON.parse(txt);
  }

  // ╔══════════════════════════════════════════════════════════════════╗
  // ║  EJECUCIÓN PRINCIPAL                                            ║
  // ╚══════════════════════════════════════════════════════════════════╝

  console.log('');
  console.log('╔═══════════════════════════════════════════════════╗');
  console.log('║  Val-Débarras — Migración HTML → WordPress        ║');
  console.log('╚═══════════════════════════════════════════════════╝');
  console.log(`📡 Vercel: ${VERCEL_BASE_URL}`);
  console.log(`📄 Páginas: ${PAGES.length} (incluye 36 canton + 36 merci + 6 servicio + 1 merci genérica)`);
  console.log('');

  let ok = 0, fail = 0, skip = 0;
  const errors = [];

  for (let i = 0; i < PAGES.length; i++) {
    const page = PAGES[i];
    const label = [page.grandparentSlug, page.parentSlug, page.slug].filter(Boolean).join('/');
    const progress = `[${String(i + 1).padStart(2)}/${PAGES.length}]`;

    // 1. Buscar WP page ID
    let wpId;
    try {
      wpId = await getPageId(page.slug, page.parentSlug, page.grandparentSlug);
    } catch (e) {
      console.error(`❌ ${progress} ${label} — Error buscando ID: ${e.message}`);
      errors.push({ label, error: 'ID lookup: ' + e.message });
      fail++;
      continue;
    }

    if (!wpId) {
      console.warn(`⚠️  ${progress} ${label} — Página WP no encontrada, skip`);
      skip++;
      continue;
    }

    // 2. Descargar HTML desde Vercel
    let html;
    try {
      const srcUrl = VERCEL_BASE_URL + page.src + '/';
      const resp = await fetch(srcUrl);
      if (!resp.ok) throw new Error(`HTTP ${resp.status} al buscar ${srcUrl}`);
      html = await resp.text();
      if (html.length < 500) throw new Error(`HTML muy corto (${html.length} chars) — posible error`);
    } catch (e) {
      console.error(`❌ ${progress} ${label} — Error descargando: ${e.message}`);
      errors.push({ label, error: 'Fetch: ' + e.message });
      fail++;
      continue;
    }

    // 3. Guardar en WP
    try {
      await updatePageMeta(wpId, html);
      console.log(`✅ ${progress} ${label} → WP ID ${wpId} (${(html.length / 1024).toFixed(0)} KB)`);
      ok++;
    } catch (e) {
      console.error(`❌ ${progress} ${label} — Error guardando: ${e.message}`);
      errors.push({ label, error: 'Save: ' + e.message });
      fail++;
    }

    await delay(DELAY_MS);
  }

  // ── Resumen ───────────────────────────────────────────────────────
  console.log('');
  console.log('╔═══════════════════════════════════════════════════╗');
  console.log('║  RESUMEN                                          ║');
  console.log('╚═══════════════════════════════════════════════════╝');
  console.log(`  ✅ OK     : ${ok}`);
  console.log(`  ⚠️  Skip  : ${skip}`);
  console.log(`  ❌ Error  : ${fail}`);

  if (errors.length > 0) {
    console.log('\n🔴 Errores:');
    errors.forEach(e => console.log(`   ${e.label} — ${e.error}`));
    console.log('\nCorrige los errores y vuelve a correr solo las páginas fallidas.');
  }

  if (ok > 0 && fail === 0) {
    console.log('\n🎉 Migración completada con éxito.');
    console.log('   Verifica en: https://www.val-debarras.ch/debarras-appartement/geneve/');
  }
})();
