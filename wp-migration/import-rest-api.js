/**
 * Val-Débarras — Import automatisé via WP REST API
 * Crée la structure hiérarchique : /service/ → /service/canton/ → /service/canton/merci/
 *
 * Prérequis :
 *   node >= 16
 *   npm install node-fetch@2
 *
 * Usage :
 *   WP_USER=votre_username WP_PASS="3on3 nA38 tflT Qy2x A2xt a1TK" node import-rest-api.js
 *
 * Idempotent : peut être relancé sans danger, skip les pages existantes.
 */

const fetch = require('node-fetch');

const WP_URL  = 'https://www.val-debarras.ch';
const WP_USER = process.env.WP_USER || 'admin';
const WP_PASS = process.env.WP_PASS || '';

if (!WP_PASS) {
  console.error('Erreur: WP_PASS requis.\nUsage: WP_USER=admin WP_PASS="xxxx xxxx..." node import-rest-api.js');
  process.exit(1);
}

const AUTH = Buffer.from(`${WP_USER}:${WP_PASS}`).toString('base64');
const HEADERS = {
  'Authorization': `Basic ${AUTH}`,
  'Content-Type': 'application/json',
};

// ── Data — slugs identiques aux URLs cibles du client ────────────────────────

const SERVICES = [
  {
    slug: 'debarras-appartement',
    title: 'Débarras appartement en Suisse romande',
    nom: 'Débarras appartement',
    desc: 'appartement',
    metaDesc: 'Débarras appartement en Suisse romande avec Val-Débarras. Intervention rapide, devis gratuit. ☎ 079 580 58 57',
  },
  {
    slug: 'debarras-maison',
    title: 'Débarras maison en Suisse romande',
    nom: 'Débarras maison',
    desc: 'maison',
    metaDesc: 'Débarras maison en Suisse romande avec Val-Débarras. Intervention rapide, devis gratuit. ☎ 079 580 58 57',
  },
  {
    slug: 'debarras-apres-deces-succession',
    title: 'Débarras après décès / succession en Suisse romande',
    nom: 'Débarras après décès / succession',
    desc: 'succession',
    metaDesc: 'Débarras après décès et succession en Suisse romande. Intervention discrète et rapide. Devis gratuit. ☎ 079 580 58 57',
  },
  {
    slug: 'debarras-ems',
    title: 'Débarras suite à entrée en EMS — Suisse romande',
    nom: 'Débarras EMS',
    desc: 'logement suite à entrée en EMS',
    metaDesc: 'Débarras suite à entrée en EMS en Suisse romande. Intervention rapide, devis gratuit. ☎ 079 580 58 57',
  },
  {
    slug: 'debarras-insalubre-diogene',
    title: 'Débarras insalubre / Diogène en Suisse romande',
    nom: 'Débarras insalubre / Diogène',
    desc: 'logement insalubre ou syndrome de Diogène',
    metaDesc: 'Débarras logement insalubre et syndrome de Diogène en Suisse romande. Discrétion garantie. ☎ 079 580 58 57',
  },
  {
    slug: 'nettoyage-extreme',
    title: 'Nettoyage extrême en Suisse romande',
    nom: 'Nettoyage extrême',
    desc: 'nettoyage extrême',
    metaDesc: 'Nettoyage extrême et remise en état en Suisse romande. Intervention rapide, devis gratuit. ☎ 079 580 58 57',
  },
];

const CANTONS = [
  {
    slug: 'geneve',
    nom: 'Genève',
    code: 'ge',
    prep: 'à',
    communes: 'Genève, Carouge, Lancy, Vernier, Meyrin, Onex, Thônex, Plan-les-Ouates, Bernex, Chêne-Bougeries',
  },
  {
    slug: 'vaud',
    nom: 'Vaud',
    code: 'vd',
    prep: 'dans le canton de',
    communes: 'Lausanne, Morges, Nyon, Yverdon-les-Bains, Renens, Prilly, Pully, Gland, Rolle, Aigle',
  },
  {
    slug: 'valais',
    nom: 'Valais',
    code: 'vs',
    prep: 'en',
    communes: 'Sion, Sierre, Martigny, Monthey, Visp, Brig, Naters, Leuk, Saas-Fee, Verbier',
  },
  {
    slug: 'fribourg',
    nom: 'Fribourg',
    code: 'fr',
    prep: 'à',
    communes: 'Fribourg, Bulle, Romont, Murten, Estavayer-le-Lac, Châtel-Saint-Denis, Villars-sur-Glâne',
  },
  {
    slug: 'neuchatel',
    nom: 'Neuchâtel',
    code: 'ne',
    prep: 'à',
    communes: 'Neuchâtel, La Chaux-de-Fonds, Le Locle, Boudry, Fleurier, Couvet, Peseux, Colombier',
  },
  {
    slug: 'jura',
    nom: 'Jura',
    code: 'ju',
    prep: 'au',
    communes: 'Delémont, Porrentruy, Saignelégier, Bassecourt, Courrendlin, Courfaivre, Moutier',
  },
];

// ── Helpers ───────────────────────────────────────────────────────────────────

async function wpGet(endpoint) {
  const r = await fetch(`${WP_URL}/wp-json/wp/v2/${endpoint}`, { headers: HEADERS });
  return { status: r.status, body: await r.json() };
}

async function wpPost(endpoint, data) {
  const r = await fetch(`${WP_URL}/wp-json/wp/v2/${endpoint}`, {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(data),
  });
  return { status: r.status, body: await r.json() };
}

async function findPageBySlug(slug, parent = 0) {
  const query = parent ? `pages?slug=${slug}&parent=${parent}&status=any` : `pages?slug=${slug}&status=any`;
  const r = await wpGet(query);
  if (r.status === 200 && r.body.length > 0) return r.body[0];
  return null;
}

async function createOrSkipPage(data) {
  const existing = await findPageBySlug(data.slug, data.parent || 0);
  if (existing) return { id: existing.id, created: false };

  const r = await wpPost('pages', data);
  if (r.status === 201) return { id: r.body.id, created: true };

  throw new Error(`HTTP ${r.status}: ${JSON.stringify(r.body).substring(0, 200)}`);
}

function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── Content builders ──────────────────────────────────────────────────────────

function buildServiceContent(svc) {
  return `<!-- wp:paragraph -->
<p>Val-Débarras est votre spécialiste du ${svc.desc} en Suisse romande. Notre équipe intervient rapidement dans les cantons de Genève, Vaud, Valais, Fribourg, Neuchâtel et Jura.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Nos interventions de ${svc.nom.toLowerCase()}</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>Devis gratuit et sans engagement</li>
<li>Intervention rapide — délai garanti</li>
<li>Équipe professionnelle et discrète</li>
<li>Rachat du mobilier possible</li>
<li>Don aux associations caritatives (Caritas, Emmaus)</li>
<li>Évacuation des déchets conforme aux normes suisses</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {"level":2} -->
<h2>Nos zones d'intervention</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Nous intervenons dans toute la Suisse romande : <a href="/debarras-appartement/geneve/">Genève</a>, <a href="/debarras-appartement/vaud/">Vaud</a>, <a href="/debarras-appartement/valais/">Valais</a>, <a href="/debarras-appartement/fribourg/">Fribourg</a>, <a href="/debarras-appartement/neuchatel/">Neuchâtel</a>, <a href="/debarras-appartement/jura/">Jura</a>.</p>
<!-- /wp:paragraph -->`;
}

function buildCantonContent(svc, canton) {
  return `<!-- wp:paragraph -->
<p>Val-Débarras est votre spécialiste du ${svc.desc} ${canton.prep} ${canton.nom}. Notre équipe intervient rapidement, avec professionnalisme et discrétion dans tout le canton.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Pourquoi choisir Val-Débarras ${canton.prep} ${canton.nom} ?</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>Intervention rapide — délai garanti</li>
<li>Équipe professionnelle et discrète</li>
<li>Devis gratuit et sans engagement</li>
<li>Rachat du mobilier possible</li>
<li>Don aux associations caritatives (Caritas, Emmaus)</li>
<li>Évacuation des déchets conforme aux normes suisses</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {"level":2} -->
<h2>Notre zone d'intervention ${canton.prep} ${canton.nom}</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Nous intervenons dans tout le canton de ${canton.nom} : ${canton.communes}.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Questions fréquentes</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Quel est le prix d'un ${svc.desc} ${canton.prep} ${canton.nom} ?</strong><br>Le prix dépend du volume, de l'accessibilité et de l'urgence. Contactez-nous pour un devis gratuit sous 24h.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Combien de temps dure l'intervention ?</strong><br>En général 1 à 3 jours selon la taille du logement. Nous vous donnons une estimation précise lors du devis.</p>
<!-- /wp:paragraph -->`;
}

function buildMerciContent(svc, canton) {
  return `<!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center">Votre demande de <strong>${svc.desc} ${canton.prep} ${canton.nom}</strong> a bien été enregistrée.<br>Un spécialiste Val-Débarras va vous rappeler dans les meilleurs délais.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"align":"center"} -->
<p class="has-text-align-center">Une urgence ? <a href="tel:+41795805857">079 580 58 57</a></p>
<!-- /wp:paragraph -->`;
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log('=== Val-Débarras WP Import — Structure hiérarchique ===\n');
  console.log('Structure cible :');
  console.log('  /service/         → page générique service');
  console.log('  /service/canton/  → page canton');
  console.log('  /service/canton/merci/  → page merci (conversion Google Ads)\n');

  // Test connexion
  const me = await wpGet('users/me');
  if (me.status !== 200) {
    console.error(`Connexion échouée (HTTP ${me.status}): ${JSON.stringify(me.body)}`);
    process.exit(1);
  }
  console.log(`✓ Connecté : ${me.body.name}\n`);

  let created = 0;
  let skipped = 0;
  let errors  = 0;

  for (const svc of SERVICES) {
    console.log(`\n── Service : ${svc.slug} ──`);

    // 1. Page générique service (parent)
    let serviceId;
    try {
      const r = await createOrSkipPage({
        title: svc.title,
        slug:  svc.slug,
        status: 'publish',
        content: buildServiceContent(svc),
        meta: { _yoast_wpseo_metadesc: svc.metaDesc },
      });
      serviceId = r.id;
      if (r.created) {
        console.log(`  ✓ Créé : /${svc.slug}/  (ID ${serviceId})`);
        created++;
      } else {
        console.log(`  ↷ Existe : /${svc.slug}/  (ID ${serviceId})`);
        skipped++;
      }
    } catch (e) {
      console.error(`  ✗ ERREUR page service ${svc.slug}: ${e.message}`);
      errors++;
      continue;
    }
    await delay(400);

    // 2. Pages canton (enfants du service)
    for (const canton of CANTONS) {
      const cantonTitle   = `${svc.nom} ${canton.prep} ${canton.nom} — Val-Débarras`;
      const cantonMetaDesc = `${svc.nom} ${canton.prep} ${canton.nom} avec Val-Débarras. Devis gratuit, intervention rapide. ☎ 079 580 58 57`;

      let cantonId;
      try {
        const r = await createOrSkipPage({
          title:  cantonTitle,
          slug:   canton.slug,
          parent: serviceId,
          status: 'publish',
          content: buildCantonContent(svc, canton),
          meta: {
            _yoast_wpseo_metadesc: cantonMetaDesc,
            canton_nom:   canton.nom,
            canton_code:  canton.code,
            service_nom:  svc.nom,
            service_slug: svc.slug,
            communes_pills: canton.communes,
          },
        });
        cantonId = r.id;
        if (r.created) {
          console.log(`    ✓ Créé : /${svc.slug}/${canton.slug}/  (ID ${cantonId})`);
          created++;
        } else {
          console.log(`    ↷ Existe : /${svc.slug}/${canton.slug}/  (ID ${cantonId})`);
          skipped++;
        }
      } catch (e) {
        console.error(`    ✗ ERREUR ${svc.slug}/${canton.slug}: ${e.message}`);
        errors++;
        continue;
      }
      await delay(300);

      // 3. Page merci (enfant du canton) — landing page Google Ads conversion
      try {
        const r = await createOrSkipPage({
          title:  `Merci — ${svc.nom} ${canton.prep} ${canton.nom}`,
          slug:   'merci',
          parent: cantonId,
          status: 'publish',
          content: buildMerciContent(svc, canton),
          meta: { _yoast_wpseo_noindex: '1' }, // noindex pour ne pas diluer le SEO
        });
        if (r.created) {
          console.log(`      ✓ Créé : /${svc.slug}/${canton.slug}/merci/  (ID ${r.id})`);
          created++;
        } else {
          console.log(`      ↷ Existe : /${svc.slug}/${canton.slug}/merci/`);
          skipped++;
        }
      } catch (e) {
        console.error(`      ✗ ERREUR merci ${svc.slug}/${canton.slug}: ${e.message}`);
        errors++;
      }
      await delay(300);
    }
  }

  console.log(`\n${'═'.repeat(50)}`);
  console.log(`  ✓ Créées  : ${created}`);
  console.log(`  ↷ Ignorées : ${skipped}`);
  console.log(`  ✗ Erreurs  : ${errors}`);
  console.log(`${'═'.repeat(50)}`);

  if (errors === 0) {
    console.log('\n✅ Import terminé sans erreur.\n');
    console.log('Étapes suivantes :');
    console.log('  1. WP Admin → Réglages → Permaliens → /%postname%/ → Enregistrer');
    console.log('  2. Installer plugin "Redirection" → importer redirects-plugin.csv');
    console.log('  3. Uploader les images (images/*.jpg, *.svg, *.png) dans la médiathèque');
    console.log('  4. Activer le thème enfant et importer le formulaire CF7');
    console.log('  5. Tester toutes les URLs : node verify-urls.js');
    console.log('  6. Mettre à jour les URLs finales dans Google Ads');
  } else {
    console.log('\n⚠️  Des erreurs ont eu lieu. Corriger et relancer (le script est idempotent).');
  }
}

main().catch(err => {
  console.error('Erreur fatale:', err);
  process.exit(1);
});
