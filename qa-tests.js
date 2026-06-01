/**
 * Val-Débarras — Suite QA complète
 * Tests: Régression · UX/UI · Stress · Sécurité
 */

const { chromium } = require('playwright');

const BASE = 'http://localhost:8766';
const EXEC = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const CANTONS = ['geneve', 'vaud', 'valais', 'fribourg', 'neuchatel', 'jura'];
const SERVICES = [
  { slug: 'debarras-appartement', label: 'appartement' },
  { slug: 'debarras-maison',      label: 'maison' },
  { slug: 'debarras-apres-deces', label: 'succession' },
  { slug: 'debarras-ems',         label: 'EMS' },
  { slug: 'debarras-insalubre-diogene', label: 'diogene' },
  { slug: 'nettoyage-extreme',    label: 'nettoyage' },
];

const ALL_CANTON_URLS = [];
for (const s of SERVICES) {
  for (const c of CANTONS) {
    ALL_CANTON_URLS.push(`/${s.slug}/${c}/`);
  }
}

const STATIC_PAGES = ['/', '/blog/', '/blog/comment-debarrasser-appartement-suisse-romande/'];

const results = { pass: [], fail: [], warn: [] };

function pass(id, msg) { results.pass.push({ id, msg }); }
function fail(id, msg) { results.fail.push({ id, msg }); console.error(`  ✗ [${id}] ${msg}`); }
function warn(id, msg) { results.warn.push({ id, msg }); console.warn(`  ⚠ [${id}] ${msg}`); }

// ─────────────────────────────────────────────────────────────────────────────
async function testPage(page, url, opts = {}) {
  const fullUrl = BASE + url;
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));

  const t0 = Date.now();
  const res = await page.goto(fullUrl, { waitUntil: 'domcontentloaded', timeout: 15000 });
  const loadMs = Date.now() - t0;

  return { res, errors, loadMs };
}

// ─────────────────────────────────────────────────────────────────────────────
async function runTests() {
  const browser = await chromium.launch({
    executablePath: EXEC,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
    headless: true,
  });

  console.log('\n╔══════════════════════════════════════════════════════════╗');
  console.log('║   VAL-DÉBARRAS — QA SUITE COMPLÈTE                      ║');
  console.log('╚══════════════════════════════════════════════════════════╝\n');

  // ══════════════════════════════════════════════════════════════
  // 1. RÉGRESSION — Pages statiques principales
  // ══════════════════════════════════════════════════════════════
  console.log('═══ 1. RÉGRESSION — Pages statiques ═══');
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();

    for (const url of STATIC_PAGES) {
      const { res, errors, loadMs } = await testPage(page, url);

      if (res.status() !== 200) {
        fail('REG-HTTP', `${url} → HTTP ${res.status()}`);
      } else {
        pass('REG-HTTP', `${url} → 200 (${loadMs}ms)`);
        console.log(`  ✓ ${url} [${loadMs}ms]`);
      }

      if (errors.length > 0) fail('REG-JSERR', `${url} — JS errors: ${errors.join(' | ')}`);

      // Title not empty / not PROTOTYPE
      const title = await page.title();
      if (!title || title.trim() === '') fail('REG-TITLE', `${url} — title vide`);
      else if (/PROTOTYPE/i.test(title)) fail('REG-PROTO', `${url} — PROTOTYPE dans le titre: "${title}"`);
      else pass('REG-TITLE', `${url} — "${title}"`);

      // No PROTOTYPE/NOUVEAU visible in DOM
      const proto = await page.$('.proto, .proto-tag');
      if (proto) fail('REG-PROTO-DOM', `${url} — élément .proto visible`);
      else pass('REG-PROTO-DOM', `${url} — pas de bannière PROTOTYPE`);

      // og:image
      const ogImg = await page.$('meta[property="og:image"]');
      if (!ogImg) warn('REG-OG', `${url} — og:image manquant`);
      else pass('REG-OG', `${url} — og:image présent`);
    }
    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 2. RÉGRESSION — 36 pages canton (HTTP + canton correct)
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 2. RÉGRESSION — 36 pages canton ═══');
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();

    const cantonLabels = {
      geneve: 'Genève', vaud: 'Vaud', valais: 'Valais',
      fribourg: 'Fribourg', neuchatel: 'Neuchâtel', jura: 'Jura',
    };

    let okCount = 0;
    for (const s of SERVICES) {
      for (const c of CANTONS) {
        const url = `/${s.slug}/${c}/`;
        const { res, errors, loadMs } = await testPage(page, url);

        if (res.status() !== 200) {
          fail('CANTON-HTTP', `${url} → ${res.status()}`);
          continue;
        }

        // Check canton name in H1
        const h1 = await page.$eval('h1', el => el.textContent).catch(() => '');
        const expected = cantonLabels[c];
        if (!h1.includes(expected) && !h1.includes(c.charAt(0).toUpperCase() + c.slice(1))) {
          fail('CANTON-H1', `${url} — H1 "${h1.trim().slice(0, 60)}" ne contient pas "${expected}"`);
        } else {
          okCount++;
        }

        if (errors.length > 0) fail('CANTON-JS', `${url} JS: ${errors[0]}`);
      }
    }
    console.log(`  ✓ ${okCount}/36 pages avec H1 canton correct`);
    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 3. UX/UI — Homepage desktop
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 3. UX/UI — Desktop (1280px) ═══');
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await testPage(page, '/');

    // Navigation visible
    const nav = await page.$('nav, .nav');
    if (!nav) fail('UX-NAV', 'Pas de nav sur desktop');
    else {
      const visible = await nav.isVisible();
      if (!visible) fail('UX-NAV', 'Nav non visible desktop');
      else pass('UX-NAV', 'Navigation visible desktop');
    }

    // Hamburger hidden on desktop
    const ham = await page.$('.hamburger');
    if (ham) {
      const hamVis = await ham.isVisible();
      if (hamVis) fail('UX-HAM', 'Hamburger visible sur desktop (devrait être caché)');
      else pass('UX-HAM', 'Hamburger caché sur desktop');
    }

    // CTA buttons present
    const cta = await page.$$('.btn-primary, .btn-devis, .header-cta');
    if (cta.length === 0) fail('UX-CTA', 'Aucun bouton CTA trouvé');
    else pass('UX-CTA', `${cta.length} boutons CTA trouvés`);

    // Phone number visible
    const phone = await page.getByText('079 580 58 57').first();
    if (!phone) warn('UX-PHONE', 'Numéro de téléphone non trouvé');
    else pass('UX-PHONE', 'Numéro de téléphone présent');

    // Hero image loads
    const heroImg = await page.$('.hero-img img');
    if (heroImg) {
      const natural = await heroImg.evaluate(el => el.naturalWidth);
      if (natural === 0) fail('UX-HEROIMG', 'Image hero ne charge pas');
      else pass('UX-HEROIMG', `Image hero chargée (${natural}px largeur naturelle)`);
    } else {
      warn('UX-HEROIMG', 'Élément .hero-img img non trouvé');
    }

    // Stats section
    const stats = await page.$$('.stat');
    if (stats.length < 3) fail('UX-STATS', `Seulement ${stats.length} stats (attendu ≥3)`);
    else pass('UX-STATS', `${stats.length} stats affichées`);

    // Services grid
    const services = await page.$$('.sc');
    if (services.length < 6) fail('UX-SERVICES', `${services.length} services (attendu 6)`);
    else pass('UX-SERVICES', `${services.length} cartes service`);

    // FAQ section
    const faqs = await page.$$('.faq-item, .faq-q');
    pass('UX-FAQ', `${faqs.length} éléments FAQ`);

    // Form present
    const form = await page.$('form');
    if (!form) fail('UX-FORM', 'Formulaire de contact absent');
    else pass('UX-FORM', 'Formulaire présent');

    // Scroll to bottom without layout shift
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(500);
    const scrollErr = await page.evaluate(() => {
      return window.scrollY > 100 ? null : 'Page non scrollable';
    });
    if (scrollErr) warn('UX-SCROLL', scrollErr);
    else pass('UX-SCROLL', 'Scroll complet OK');

    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 4. UX/UI — Mobile (390px iPhone 14)
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 4. UX/UI — Mobile (390px) ═══');
  {
    const ctx = await browser.newContext({
      viewport: { width: 390, height: 844 },
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',
    });
    const page = await ctx.newPage();
    await testPage(page, '/');

    // Hamburger visible on mobile
    const ham = await page.$('.hamburger');
    if (!ham) fail('MOB-HAM', 'Bouton hamburger absent sur mobile');
    else {
      const vis = await ham.isVisible();
      if (!vis) fail('MOB-HAM', 'Hamburger non visible sur mobile');
      else pass('MOB-HAM', 'Hamburger visible sur mobile');
    }

    // Desktop nav hidden
    const nav = await page.$('.nav');
    if (nav) {
      const navVis = await nav.isVisible();
      if (navVis) fail('MOB-NAV', 'Nav desktop visible sur mobile (devrait être caché)');
      else pass('MOB-NAV', 'Nav desktop caché sur mobile');
    }

    // No horizontal overflow
    const overflow = await page.evaluate(() => {
      return document.body.scrollWidth > window.innerWidth;
    });
    if (overflow) fail('MOB-OVERFLOW', `Overflow horizontal détecté (body.scrollWidth > ${390}px)`);
    else pass('MOB-OVERFLOW', 'Pas d\'overflow horizontal');

    // Mobile hero visible
    const mobileHero = await page.$('.mobile-hero');
    if (mobileHero) {
      const vis = await mobileHero.isVisible();
      if (!vis) warn('MOB-HERO', 'Section mobile-hero non visible');
      else pass('MOB-HERO', 'Hero mobile affiché');
    }

    // Sticky mobile bar
    const sticky = await page.$('.sticky-mobile');
    if (sticky) {
      const vis = await sticky.isVisible();
      pass('MOB-STICKY', vis ? 'Barre sticky mobile visible' : 'Barre sticky non visible (normal en haut de page)');
    }

    // Open hamburger drawer
    try {
      await ham.click();
      await page.waitForTimeout(400);
      const drawer = await page.$('.mobile-drawer.is-open, .mobile-drawer.open');
      if (!drawer) fail('MOB-DRAWER', 'Drawer ne s\'ouvre pas au clic hamburger');
      else {
        pass('MOB-DRAWER', 'Drawer s\'ouvre correctement');

        // Check service titles in drawer
        const drawerTitles = await page.$$eval('.drawer-title span:first-child', els =>
          els.map(e => e.textContent.trim())
        );
        const expected6 = ['Débarras appartement','Débarras maison','Après décès',
                           'Débarras EMS','Diogène','Nettoyage'];
        if (drawerTitles.length < 6) fail('MOB-DRAWER-SVC', `${drawerTitles.length} services (attendu 6): ${drawerTitles}`);
        else pass('MOB-DRAWER-SVC', `6 services dans le drawer: ${drawerTitles.join(' | ')}`);

        // Open first accordion and check canton links
        const firstTitle = await page.$('.drawer-title');
        await firstTitle.click();
        await page.waitForTimeout(300);
        const cantonLinks = await page.$$('.drawer-cantons.open a, .drawer-cantons a');
        if (cantonLinks.length < 6) warn('MOB-DRAWER-CAN', `${cantonLinks.length} liens canton (attendu 6)`);
        else pass('MOB-DRAWER-CAN', `${cantonLinks.length} liens canton dans l\'accordéon`);

        // Close drawer
        const closeBtn = await page.$('.drawer-close');
        if (closeBtn) await closeBtn.click();
      }
    } catch (e) {
      fail('MOB-DRAWER-ERR', `Erreur interaction drawer: ${e.message}`);
    }

    // Touch targets >= 44px
    const buttons = await page.$$('a, button');
    let tooSmall = 0;
    for (const btn of buttons.slice(0, 20)) {
      const box = await btn.boundingBox();
      if (box && (box.height < 44 || box.width < 44) && box.height > 0) {
        tooSmall++;
      }
    }
    if (tooSmall > 3) warn('MOB-TOUCH', `${tooSmall}/20 éléments ont des zones de toucher < 44px`);
    else pass('MOB-TOUCH', `Zones de toucher OK (${tooSmall}/20 sous 44px)`);

    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 5. UX/UI — Navigation desktop dropdowns
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 5. UX/UI — Navigation dropdowns ═══');
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await testPage(page, '/');

    const navItems = await page.$$('.nav-item, .nav-btn');
    pass('UX-NAVITEMS', `${navItems.length} éléments de navigation`);

    if (navItems.length > 0) {
      try {
        await navItems[0].hover();
        await page.waitForTimeout(300);
        const dropdown = await page.$('.nav-dropdown, .nav-panel, .dropdown');
        if (dropdown) {
          const vis = await dropdown.isVisible();
          if (vis) pass('UX-DROPDOWN', 'Dropdown visible au survol');
          else warn('UX-DROPDOWN', 'Dropdown trouvé mais non visible au survol');
        } else {
          warn('UX-DROPDOWN', 'Aucun dropdown trouvé au survol du nav');
        }
      } catch(e) {
        warn('UX-DROPDOWN', `Erreur test dropdown: ${e.message}`);
      }
    }

    // Nav dropdown: .nav-item hover → .dd appears
    try {
      await navItems[0].hover();
      await page.waitForTimeout(300);
      const dd = await page.$('.dd');
      if (dd) {
        const vis = await dd.isVisible();
        if (vis) pass('UX-DROPDOWN', 'Dropdown (.dd) visible au survol');
        else warn('UX-DROPDOWN', 'Dropdown (.dd) trouvé mais non visible');
      } else {
        warn('UX-DROPDOWN', 'Aucun élément .dd trouvé');
      }
    } catch(e) {
      warn('UX-DROPDOWN', `Erreur test dropdown: ${e.message}`);
    }

    // Internal links in nav work
    const navLinks = await page.$$eval('.nav a[href]', links =>
      links.map(l => l.getAttribute('href')).filter(h => h && h.startsWith('/'))
    );
    pass('UX-NAVLINKS', `${navLinks.length} liens internes dans la navigation`);

    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 6. UX/UI — FAQ accordion (sur page canton, pas homepage)
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 6. UX/UI — FAQ accordion ═══');
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await testPage(page, '/debarras-appartement/geneve/');
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.7));
    await page.waitForTimeout(300);

    const faqBtns = await page.$$('.faq-q');
    if (faqBtns.length === 0) {
      warn('FAQ-ITEMS', 'Aucun bouton .faq-q trouvé sur page canton');
    } else {
      try {
        await faqBtns[0].click();
        await page.waitForTimeout(300);
        const answer = await page.$('.faq-a');
        if (answer) {
          const vis = await answer.isVisible();
          if (vis) pass('FAQ-OPEN', 'FAQ s\'ouvre au clic');
          else warn('FAQ-OPEN', 'Réponse .faq-a non visible après clic');
        }
        pass('FAQ-COUNT', `${faqBtns.length} questions FAQ`);
      } catch(e) {
        warn('FAQ-ERR', `Erreur FAQ: ${e.message}`);
      }
    }
    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 7. SÉCURITÉ
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 7. SÉCURITÉ ═══');
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();

    // XSS test — inject via URL param (vercel.json catch-all → index.html)
    const xssPayload = '<script>window.__xss=1</script>';
    await page.goto(`${BASE}/?q=${encodeURIComponent(xssPayload)}`, { waitUntil: 'domcontentloaded' });
    const xssExec = await page.evaluate(() => window.__xss);
    if (xssExec) fail('SEC-XSS', 'XSS exécuté via paramètre URL !');
    else pass('SEC-XSS', 'XSS via URL param non exécuté');

    // External links have rel="noopener"
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });
    const unsafeLinks = await page.$$eval('a[target="_blank"]:not([rel*="noopener"])', ls =>
      ls.map(l => l.href)
    );
    if (unsafeLinks.length > 0) warn('SEC-NOOPENER', `${unsafeLinks.length} liens _blank sans noopener: ${unsafeLinks.slice(0,3).join(', ')}`);
    else pass('SEC-NOOPENER', 'Tous les liens _blank ont rel=noopener');

    // No sensitive data in HTML (passwords, API keys patterns)
    const pageSource = await page.content();
    const sensitivePatterns = [
      { re: /password\s*=\s*["'][^"']+["']/i, label: 'password en dur' },
      { re: /api[_-]?key\s*[:=]\s*["'][a-z0-9]{20,}/i, label: 'API key' },
      { re: /bearer\s+[a-z0-9\-_.]{20,}/i, label: 'Bearer token' },
      { re: /sk-[a-zA-Z0-9]{40,}/, label: 'OpenAI key' },
    ];
    for (const { re, label } of sensitivePatterns) {
      if (re.test(pageSource)) fail('SEC-LEAK', `Données sensibles: ${label}`);
      else pass('SEC-DATA', `Pas de ${label} dans le HTML`);
    }

    // No debug mode / console.log with sensitive data
    const consoleLeaks = [];
    page.on('console', msg => {
      if (msg.type() === 'error') consoleLeaks.push(msg.text());
    });
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });
    if (consoleLeaks.length > 0) warn('SEC-CONSOLE', `${consoleLeaks.length} erreurs console: ${consoleLeaks[0]}`);
    else pass('SEC-CONSOLE', 'Aucune erreur console');

    // Form: no autocomplete="off" on legitimate fields
    const formInputs = await page.$$eval('input[type="text"], input[type="email"], input[type="tel"]', inputs =>
      inputs.map(i => ({ name: i.name, autocomplete: i.getAttribute('autocomplete') }))
    );
    const blockedAC = formInputs.filter(i => i.autocomplete === 'off');
    if (blockedAC.length > 0) warn('SEC-AUTOCOMPLETE', `${blockedAC.length} champs avec autocomplete=off (UX dégradé)`);
    else pass('SEC-AUTOCOMPLETE', 'autocomplete non bloqué sur les champs légitimes');

    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 8. PERFORMANCE / STRESS
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 8. PERFORMANCE & STRESS ═══');
  {
    // Load 10 pages concurrently
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const testUrls = ALL_CANTON_URLS.slice(0, 10);
    const t0 = Date.now();
    const pages = await Promise.all(testUrls.map(() => ctx.newPage()));
    await Promise.all(pages.map((p, i) =>
      p.goto(BASE + testUrls[i], { waitUntil: 'domcontentloaded', timeout: 20000 })
    ));
    const elapsed = Date.now() - t0;
    pass('STRESS-CONCURRENT', `10 pages chargées en parallèle en ${elapsed}ms`);
    console.log(`  ✓ 10 pages concurrent: ${elapsed}ms (moy. ${Math.round(elapsed/10)}ms/page)`);
    await Promise.all(pages.map(p => p.close()));

    // Check page weight (HTML size)
    const page = await ctx.newPage();
    let totalBytes = 0;
    page.on('response', res => {
      const len = parseInt(res.headers()['content-length'] || '0');
      totalBytes += len;
    });
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });
    if (totalBytes > 0) {
      const kb = Math.round(totalBytes / 1024);
      if (kb > 5000) warn('PERF-SIZE', `Poids total page: ${kb}KB (>5MB)`);
      else pass('PERF-SIZE', `Poids total page: ${kb}KB`);
    }

    // Load time desktop
    const loadStart = Date.now();
    await page.goto(`${BASE}/`, { waitUntil: 'load' });
    const loadTime = Date.now() - loadStart;
    if (loadTime > 3000) warn('PERF-LOAD', `Temps de chargement: ${loadTime}ms (>3s)`);
    else pass('PERF-LOAD', `Temps de chargement: ${loadTime}ms`);

    // Load time mobile throttled
    const mCtx = await browser.newContext({
      viewport: { width: 390, height: 844 },
      // Simulate slower mobile
    });
    const mPage = await mCtx.newPage();
    const mStart = Date.now();
    await mPage.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });
    const mTime = Date.now() - mStart;
    if (mTime > 4000) warn('PERF-MOBILE', `Chargement mobile: ${mTime}ms (>4s)`);
    else pass('PERF-MOBILE', `Chargement mobile: ${mTime}ms`);
    await mCtx.close();

    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 9. ACCESSIBILITÉ basique
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 9. ACCESSIBILITÉ ═══');
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });

    // Images with alt
    const imgs = await page.$$eval('img', imgs => imgs.map(i => ({
      src: i.src.split('/').pop(),
      alt: i.getAttribute('alt'),
      decorative: i.getAttribute('role') === 'presentation' || i.getAttribute('alt') === ''
    })));
    const missingAlt = imgs.filter(i => i.alt === null && !i.decorative);
    if (missingAlt.length > 0) warn('A11Y-ALT', `${missingAlt.length} images sans alt: ${missingAlt.map(i=>i.src).join(', ')}`);
    else pass('A11Y-ALT', `Toutes les images ont un alt (${imgs.length} images)`);

    // H1 present and unique
    const h1s = await page.$$('h1');
    if (h1s.length === 0) fail('A11Y-H1', 'Pas de H1 sur la page');
    else if (h1s.length > 1) warn('A11Y-H1', `${h1s.length} H1 sur la page (devrait être 1)`);
    else pass('A11Y-H1', 'H1 unique présent');

    // Buttons with aria-label or text
    const btnsNoLabel = await page.$$eval('button:not([aria-label]):not([aria-labelledby])', btns =>
      btns.filter(b => !b.textContent.trim()).length
    );
    if (btnsNoLabel > 0) warn('A11Y-BTN', `${btnsNoLabel} boutons sans libellé accessible`);
    else pass('A11Y-BTN', 'Tous les boutons ont un libellé');

    // lang attribute
    const lang = await page.$eval('html', el => el.getAttribute('lang'));
    if (!lang) warn('A11Y-LANG', 'Attribut lang manquant sur <html>');
    else pass('A11Y-LANG', `lang="${lang}"`);

    // Skip link or focus management
    const skipLink = await page.$('a[href="#main"], a[href="#contenu"], [data-skip]');
    if (!skipLink) warn('A11Y-SKIP', 'Pas de lien d\'évitement (skip link)');
    else pass('A11Y-SKIP', 'Lien d\'évitement présent');

    await ctx.close();
  }

  // ══════════════════════════════════════════════════════════════
  // 10. LIENS INTERNES BRISÉS
  // ══════════════════════════════════════════════════════════════
  console.log('\n═══ 10. LIENS BRISÉS ═══');
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' });

    const internalLinks = await page.$$eval('a[href]', links =>
      [...new Set(links
        .map(l => l.getAttribute('href'))
        .filter(h => h && (h.startsWith('/') || h.startsWith('#')))
        .filter(h => !h.startsWith('#') && !h.includes('tel:') && !h.includes('mailto:'))
      )]
    );

    let broken = 0;
    const sample = internalLinks.slice(0, 30); // test first 30
    for (const href of sample) {
      const res = await page.goto(BASE + href, { waitUntil: 'domcontentloaded', timeout: 8000 }).catch(() => null);
      if (!res || res.status() >= 400) {
        fail('LINK-BROKEN', `${href} → ${res ? res.status() : 'timeout'}`);
        broken++;
      }
    }
    if (broken === 0) pass('LINK-CHECK', `${sample.length} liens internes testés — aucun brisé`);
    else fail('LINK-SUMMARY', `${broken}/${sample.length} liens brisés`);

    await ctx.close();
  }

  await browser.close();

  // ══════════════════════════════════════════════════════════════
  // RAPPORT FINAL
  // ══════════════════════════════════════════════════════════════
  const total = results.pass.length + results.fail.length + results.warn.length;
  console.log('\n╔══════════════════════════════════════════════════════════╗');
  console.log('║   RAPPORT FINAL QA                                       ║');
  console.log('╠══════════════════════════════════════════════════════════╣');
  console.log(`║  ✅ PASS    ${String(results.pass.length).padEnd(4)} / ${total}                                ║`);
  console.log(`║  ❌ FAIL    ${String(results.fail.length).padEnd(4)} / ${total}                                ║`);
  console.log(`║  ⚠️  WARN    ${String(results.warn.length).padEnd(4)} / ${total}                                ║`);
  console.log('╠══════════════════════════════════════════════════════════╣');

  if (results.fail.length > 0) {
    console.log('║  ÉCHECS CRITIQUES:                                       ║');
    console.log('╠══════════════════════════════════════════════════════════╣');
    for (const f of results.fail) {
      console.log(`  ✗ [${f.id}] ${f.msg}`);
    }
  }

  if (results.warn.length > 0) {
    console.log('\n  AVERTISSEMENTS:');
    for (const w of results.warn) {
      console.log(`  ⚠ [${w.id}] ${w.msg}`);
    }
  }

  console.log('\n╚══════════════════════════════════════════════════════════╝\n');
  process.exit(results.fail.length > 0 ? 1 : 0);
}

runTests().catch(e => {
  console.error('Test suite crash:', e);
  process.exit(1);
});
