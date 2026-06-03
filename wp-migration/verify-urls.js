/**
 * Vérifie que toutes les URLs WordPress répondent 200 après l'import.
 * Usage : node verify-urls.js
 */

const fetch = require('node-fetch');

const BASE = 'https://www.val-debarras.ch';

const SERVICES = [
  'debarras-appartement',
  'debarras-maison',
  'debarras-apres-deces-succession',
  'debarras-ems',
  'debarras-insalubre-diogene',
  'nettoyage-extreme',
];

const CANTONS = ['geneve', 'vaud', 'valais', 'fribourg', 'neuchatel', 'jura'];

async function check(url) {
  try {
    const r = await fetch(url, { redirect: 'manual', timeout: 10000 });
    return r.status;
  } catch (e) {
    return `ERR: ${e.message}`;
  }
}

async function main() {
  console.log('=== Vérification des URLs Val-Débarras WP ===\n');

  const urls = [];

  // Homepage
  urls.push(`${BASE}/`);

  // Pages génériques service
  for (const svc of SERVICES) {
    urls.push(`${BASE}/${svc}/`);
  }

  // Pages canton + merci
  for (const svc of SERVICES) {
    for (const canton of CANTONS) {
      urls.push(`${BASE}/${svc}/${canton}/`);
      urls.push(`${BASE}/${svc}/${canton}/merci/`);
    }
  }

  let ok = 0;
  let fail = 0;

  for (const url of urls) {
    const status = await check(url);
    const path = url.replace(BASE, '');
    if (status === 200) {
      console.log(`  ✓ 200  ${path}`);
      ok++;
    } else {
      console.log(`  ✗ ${status}  ${path}`);
      fail++;
    }
  }

  console.log(`\n✓ OK: ${ok}  ✗ Fail: ${fail}  / Total: ${urls.length}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
