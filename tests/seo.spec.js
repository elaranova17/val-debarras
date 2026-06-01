const { test, expect } = require('@playwright/test');

const CANTON_PAGES = [
  '/ge/appartement', '/ge/maison', '/ge/succession',
  '/vd/appartement', '/vd/maison',
  '/vs/appartement',
  '/fr/appartement',
  '/ne/appartement',
  '/ju/appartement',
];

test.describe('SEO — meta tags', () => {
  test('homepage tiene meta description', async ({ page }) => {
    await page.goto('/');
    const meta = page.locator('meta[name="description"]');
    await expect(meta).toHaveCount(1);
    const content = await meta.getAttribute('content');
    expect(content?.length).toBeGreaterThan(50);
  });

  test('homepage NO tiene noindex', async ({ page }) => {
    await page.goto('/');
    const robots = page.locator('meta[name="robots"]');
    if (await robots.count() > 0) {
      const content = await robots.getAttribute('content');
      expect(content).not.toContain('noindex');
    }
  });

  test('homepage tiene og:image', async ({ page }) => {
    await page.goto('/');
    const ogImage = page.locator('meta[property="og:image"]');
    await expect(ogImage).toHaveCount(1);
    const content = await ogImage.getAttribute('content');
    expect(content).toBeTruthy();
  });

  test('homepage tiene canonical', async ({ page }) => {
    await page.goto('/');
    const canonical = page.locator('link[rel="canonical"]');
    await expect(canonical).toHaveCount(1);
  });

  test('homepage tiene un solo H1', async ({ page }) => {
    await page.goto('/');
    const h1s = page.locator('h1');
    expect(await h1s.count()).toBe(1);
  });

  for (const url of CANTON_PAGES) {
    test(`${url} tiene un solo H1`, async ({ page }) => {
      await page.goto(url);
      const h1s = page.locator('h1');
      expect(await h1s.count()).toBe(1);
    });
  }

  test('no hay páginas con PROTOTYPE o NUEVO en título', async ({ page }) => {
    await page.goto('/');
    const title = await page.title();
    expect(title.toUpperCase()).not.toContain('PROTOTYPE');
    expect(title.toUpperCase()).not.toContain('NOUVEAU');
  });
});

test.describe('SEO — rendimiento básico', () => {
  test('homepage carga en menos de 5 segundos', async ({ page }) => {
    const start = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const elapsed = Date.now() - start;
    expect(elapsed).toBeLessThan(5000);
  });

  test('todas las imágenes tienen atributo alt', async ({ page }) => {
    await page.goto('/');
    const missingAlt = await page.evaluate(() =>
      Array.from(document.images)
        .filter(img => !img.hasAttribute('alt'))
        .map(img => img.src.split('/').pop())
    );
    expect(missingAlt).toHaveLength(0);
  });
});
