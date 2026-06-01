const { defineConfig } = require('@playwright/test');

const CHROME_BIN = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const CHROME_ARGS = [
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--disable-dev-shm-usage',
  '--disable-gpu',
];

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30000,
  retries: 0,
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'playwright-report' }]],
  use: {
    baseURL: 'http://localhost:8766',
    headless: true,
    screenshot: 'only-on-failure',
    launchOptions: { executablePath: CHROME_BIN, args: CHROME_ARGS },
  },
  projects: [
    {
      name: 'Desktop Chrome',
      use: {
        viewport: { width: 1280, height: 720 },
        isMobile: false,
      },
    },
    {
      name: 'Mobile iPhone 14',
      use: {
        viewport: { width: 390, height: 844 },
        isMobile: true,
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        deviceScaleFactor: 3,
        hasTouch: true,
      },
    },
    {
      name: 'Mobile Pixel 7',
      use: {
        viewport: { width: 412, height: 915 },
        isMobile: true,
        userAgent: 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        deviceScaleFactor: 2.625,
        hasTouch: true,
      },
    },
  ],
  webServer: {
    command: 'node server.js',
    port: 8766,
    reuseExistingServer: true,
    timeout: 10000,
  },
});
