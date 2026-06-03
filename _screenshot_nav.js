const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const outDir = path.join(__dirname, 'screenshots');
  const fs = require('fs');
  fs.mkdirSync(outDir, { recursive: true });

  // Desktop 1280
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto('http://localhost:8765/index.html', { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(outDir, 'nav-desktop-1280.png'), clip: { x: 0, y: 0, width: 1280, height: 120 } });

  // Chevron close-up
  const navBtn = page.locator('.nav-btn').first();
  await navBtn.screenshot({ path: path.join(outDir, 'nav-chevron-closeup.png') });

  // Dropdown hover
  await page.locator('.nav-item').first().hover();
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(outDir, 'nav-dropdown-hover.png'), clip: { x: 0, y: 0, width: 1280, height: 350 } });

  // Mobile 390
  await page.setViewportSize({ width: 390, height: 844 });
  await page.reload({ waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(outDir, 'nav-mobile-390.png'), clip: { x: 0, y: 0, width: 390, height: 80 } });

  // Mobile hamburger click
  await page.locator('#ham').click();
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(outDir, 'nav-mobile-drawer.png'), clip: { x: 0, y: 0, width: 390, height: 500 } });

  await browser.close();
  console.log('Screenshots saved to', outDir);
})();
