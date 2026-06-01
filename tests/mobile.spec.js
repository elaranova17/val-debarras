const { test, expect } = require('@playwright/test');

// These tests run on all projects (desktop + mobile) from playwright.config.js
// but are specifically designed to catch mobile regressions

test.describe('Mobile — hero texto legible', () => {
  test('homepage: título hero no es blanco en mobile', async ({ page, isMobile }) => {
    test.skip(!isMobile, 'Solo mobile');
    await page.goto('/');
    const title = page.locator('.hero-title, .hero h1').first();
    await expect(title).toBeVisible();

    const color = await title.evaluate(el => getComputedStyle(el).color);
    const bg = await title.evaluate(el => getComputedStyle(el).backgroundColor);

    // Texto no debe ser blanco puro
    expect(color).not.toBe('rgb(255, 255, 255)');
    // Si background es blanco, texto no puede ser también blanco
    if (bg === 'rgb(255, 255, 255)' || bg === 'rgba(0, 0, 0, 0)') {
      expect(color).not.toBe('rgb(255, 255, 255)');
    }
  });

  test('hero-accent color es verde en mobile', async ({ page, isMobile }) => {
    test.skip(!isMobile, 'Solo mobile');
    await page.goto('/');
    const accent = page.locator('.hero-accent').first();
    if (await accent.count() > 0) {
      const color = await accent.evaluate(el => getComputedStyle(el).color);
      // Verde #2E7D32 = rgb(46, 125, 50)
      expect(color).toBe('rgb(46, 125, 50)');
    }
  });
});

test.describe('Mobile — layout y navegación', () => {
  test('menú hamburguesa visible en mobile', async ({ page, isMobile }) => {
    test.skip(!isMobile, 'Solo mobile');
    await page.goto('/');
    const burger = page.locator('[class*="burger"], [class*="hamburger"], .menu-toggle, #menu-btn').first();
    await expect(burger).toBeVisible();
  });

  test('no hay overflow horizontal en homepage mobile', async ({ page }) => {
    await page.goto('/');
    const overflow = await page.evaluate(() => document.body.scrollWidth > window.innerWidth + 5);
    expect(overflow).toBe(false);
  });

  test('no hay overflow horizontal en página canton mobile', async ({ page }) => {
    await page.goto('/ge/appartement');
    const overflow = await page.evaluate(() => document.body.scrollWidth > window.innerWidth + 5);
    expect(overflow).toBe(false);
  });

  test('CTA botón de contacto visible en mobile', async ({ page }) => {
    await page.goto('/');
    const cta = page.locator('a[href*="tel:"]').filter({ visible: true }).first();
    await expect(cta).toBeVisible();
  });

  test('imágenes no exceden el ancho del viewport', async ({ page }) => {
    await page.goto('/');
    const oversized = await page.evaluate(() => {
      const vw = window.innerWidth;
      return Array.from(document.images)
        .filter(img => img.getBoundingClientRect().width > vw + 5)
        .map(img => img.src);
    });
    expect(oversized).toHaveLength(0);
  });
});

test.describe('Mobile — páginas de servicio', () => {
  const pages = ['/ge/appartement', '/vd/maison', '/vs/nettoyage', '/fr/succession', '/ne/ems', '/ju/maison'];

  for (const url of pages) {
    test(`${url} — hero visible y texto legible`, async ({ page, isMobile }) => {
      test.skip(!isMobile, 'Solo mobile');
      await page.goto(url);
      const hero = page.locator('.hero').first();
      await expect(hero).toBeVisible();

      const h1 = page.locator('.hero h1, .hero-title').first();
      await expect(h1).toBeVisible();
      const color = await h1.evaluate(el => getComputedStyle(el).color);
      expect(color).not.toBe('rgb(255, 255, 255)');
    });
  }
});
