const { test, expect } = require('@playwright/test');

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
  });

  test('carga correctamente y muestra el título', async ({ page }) => {
    await expect(page).toHaveTitle(/Val-Débarras/i);
  });

  test('hero section es visible', async ({ page }) => {
    const hero = page.locator('.hero');
    await expect(hero).toBeVisible();
  });

  test('texto hero es legible (no blanco sobre blanco)', async ({ page, isMobile }) => {
    // Desktop uses .hero-desktop-h1 (a <p>); mobile uses h1.hero-title inside .mobile-hero
    const title = isMobile
      ? page.locator('h1.hero-title').first()
      : page.locator('.hero-desktop-h1').first();
    await expect(title).toBeVisible();
    const { color, hasGradientBg } = await title.evaluate(el => {
      let node = el;
      let hasGradient = false;
      let solidBg = 'rgba(0, 0, 0, 0)';
      while (node) {
        const style = getComputedStyle(node);
        const bgImg = style.backgroundImage;
        const bgColor = style.backgroundColor;
        if (bgImg && bgImg !== 'none') { hasGradient = true; break; }
        if (bgColor !== 'rgba(0, 0, 0, 0)' && bgColor !== 'transparent') {
          solidBg = bgColor;
          break;
        }
        node = node.parentElement;
      }
      return { color: getComputedStyle(el).color, hasGradientBg: hasGradient, solidBg };
    });
    // White text on white background is bad; white text on dark/gradient background is OK
    if (color === 'rgb(255, 255, 255)') {
      expect(hasGradientBg).toBe(true);
    }
  });

  test('CTA principal es clickeable', async ({ page }) => {
    const cta = page.locator('a[href*="tel:"]').filter({ visible: true }).first();
    await expect(cta).toBeVisible();
  });

  test('logo visible en el header', async ({ page }) => {
    const logo = page.locator('header img, .navbar img, nav img').first();
    await expect(logo).toBeVisible();
  });

  test('nav de servicios está presente', async ({ page }) => {
    const nav = page.locator('nav, .navbar, header').first();
    await expect(nav).toBeVisible();
  });

  test('sección de servicios visible', async ({ page }) => {
    const services = page.locator('section.services, #services');
    await expect(services).toBeVisible();
  });

  test('no hay elementos con overflow horizontal', async ({ page }) => {
    const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
    const viewportWidth = await page.evaluate(() => window.innerWidth);
    expect(bodyWidth).toBeLessThanOrEqual(viewportWidth + 5);
  });

  test('imágenes visibles cargan sin error', async ({ page }) => {
    await page.waitForLoadState('networkidle');
    const brokenImages = await page.evaluate(() => {
      return Array.from(document.images)
        .filter(img => img.loading !== 'lazy' && (!img.complete || img.naturalWidth === 0))
        .map(img => img.src);
    });
    expect(brokenImages).toHaveLength(0);
  });

  test('número de teléfono visible', async ({ page }) => {
    // footer phone button is visible on all viewport sizes
    const phone = page.locator('a.ft-phone-btn');
    await expect(phone).toBeVisible();
  });
});
