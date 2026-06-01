const { test, expect } = require('@playwright/test');

const CANTONS = ['ge', 'vd', 'vs', 'fr', 'ne', 'ju'];
const SERVICES = ['appartement', 'maison', 'succession', 'ems', 'diogene', 'nettoyage'];

test.describe('Navegación cantons', () => {
  test('homepage carga sin 404', async ({ page }) => {
    const response = await page.goto('/');
    expect(response.status()).toBe(200);
  });

  for (const canton of CANTONS) {
    test(`/${canton} responde 200`, async ({ page }) => {
      const res = await page.goto(`/${canton}`);
      expect(res.status()).toBe(200);
    });
  }

  // Sample 2 pages per canton to keep suite fast
  for (const canton of CANTONS) {
    for (const service of ['appartement', 'succession']) {
      test(`/${canton}/${service} responde 200`, async ({ page }) => {
        const res = await page.goto(`/${canton}/${service}`);
        expect(res.status()).toBe(200);
      });
    }
  }
});

test.describe('Páginas de servicio — hero image', () => {
  const sample = [
    { url: '/debarras-ems/geneve',           img: 'van-ge-ems' },
    { url: '/debarras-appartement/vaud',     img: 'van-vd-chillon' },
    { url: '/nettoyage-extreme/valais',      img: 'van-vs-sion' },
    { url: '/debarras-maison/fribourg',      img: 'van-fr-fribourg' },
    { url: '/debarras-apres-deces/neuchatel',img: 'van-ne-chateau' },
    { url: '/debarras-maison/jura',          img: 'van-ju-saintursanne' },
  ];

  for (const { url, img } of sample) {
    test(`${url} usa hero ${img}`, async ({ page }) => {
      await page.goto(url);
      const heroImg = page.locator('.hero-img img').first();
      await expect(heroImg).toBeVisible();
      const src = await heroImg.getAttribute('src');
      expect(src).toContain(img);
    });
  }
});
