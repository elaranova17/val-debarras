/**
 * Val-Débarras — Import automatisé via WP REST API
 * Exécuter depuis votre machine locale (pas depuis le cloud)
 *
 * Prérequis :
 *   node >= 16
 *   npm install node-fetch@2
 *
 * Usage :
 *   WP_USER=votre_username WP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx" node import-rest-api.js
 *
 * Le mot de passe est un Application Password WordPress (Profil → Mots de passe d'application)
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

// ── Data ─────────────────────────────────────────────────────────────────────

const SERVICES = [
  { slug: 'debarras-appartement',       nom: 'Débarras appartement' },
  { slug: 'debarras-maison',            nom: 'Débarras maison' },
  { slug: 'debarras-apres-deces',       nom: 'Après décès / succession' },
  { slug: 'debarras-ems',               nom: 'Débarras EMS' },
  { slug: 'debarras-insalubre-diogene', nom: 'Diogène & insalubre' },
  { slug: 'nettoyage-extreme',          nom: 'Nettoyage extrême' },
];

const CANTONS = [
  { slug: 'geneve',    nom: 'Genève',    code: 'ge', prep: 'à',       communes: 'Genève, Carouge, Lancy, Vernier, Meyrin, Onex, Thônex, Plan-les-Ouates, Bernex, Chêne-Bougeries' },
  { slug: 'vaud',      nom: 'Vaud',      code: 'vd', prep: 'dans le', communes: 'Lausanne, Morges, Nyon, Yverdon-les-Bains, Renens, Prilly, Pully, Gland, Rolle, Aigle' },
  { slug: 'valais',    nom: 'Valais',    code: 'vs', prep: 'en',      communes: 'Sion, Sierre, Martigny, Monthey, Visp, Brig, Naters, Leuk, Saas-Fee, Verbier' },
  { slug: 'fribourg',  nom: 'Fribourg',  code: 'fr', prep: 'à',       communes: 'Fribourg, Bulle, Romont, Murten, Estavayer-le-Lac, Châtel-Saint-Denis, Villars-sur-Glâne' },
  { slug: 'neuchatel', nom: 'Neuchâtel', code: 'ne', prep: 'à',       communes: 'Neuchâtel, La Chaux-de-Fonds, Le Locle, Boudry, Fleurier, Couvet, Peseux, Colombier' },
  { slug: 'jura',      nom: 'Jura',      code: 'ju', prep: 'au',      communes: 'Delémont, Porrentruy, Saignelégier, Bassecourt, Courrendlin, Courfaivre, Moutier' },
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

function buildContent(svc, canton) {
  return `<h2>${svc.nom} ${canton.prep} ${canton.nom}</h2>
<p>Val-Débarras est votre spécialiste du ${svc.nom.toLowerCase()} ${canton.prep} ${canton.nom} et dans toute la région. Notre équipe expérimentée intervient rapidement, avec professionnalisme et discrétion.</p>

<h3>Pourquoi choisir Val-Débarras ?</h3>
<ul>
<li>Intervention rapide — délai garanti sous 48h</li>
<li>Équipe professionnelle et discrète</li>
<li>Devis gratuit et sans engagement</li>
<li>Rachat du mobilier possible</li>
<li>Don aux associations caritatives (Caritas, Émmaüs)</li>
<li>Evacuation des déchets conforme aux normes suisses</li>
</ul>

<h3>Notre zone d'intervention ${canton.prep} ${canton.nom}</h3>
<p>Nous intervenons dans tout le canton de ${canton.nom} : ${canton.communes}.</p>

<h3>Questions fréquentes</h3>
<p><strong>Quel est le prix d'un ${svc.nom.toLowerCase()} ${canton.prep} ${canton.nom} ?</strong><br>
Le prix dépend du volume, de l'accessibilité et de l'urgence. Contactez-nous pour un devis gratuit sous 24h.</p>
<p><strong>Combien de temps dure l'intervention ?</strong><br>
En général 1 à 3 jours selon la taille du logement. Nous vous donnons une estimation précise lors du devis.</p>`;
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log('=== Val-Débarras WP REST API Import ===\n');

  // Test connexion
  const me = await wpGet('users/me');
  if (me.status !== 200) {
    console.error(`Connexion échouée (HTTP ${me.status}): ${JSON.stringify(me.body)}`);
    console.error('\nVérifiez WP_USER et WP_PASS, et assurez-vous que l\'API REST est activée.');
    process.exit(1);
  }
  console.log(`✓ Connecté en tant que: ${me.body.name} (${me.body.slug})\n`);

  let created = 0;
  let skipped = 0;
  let errors  = 0;

  for (const svc of SERVICES) {
    for (const canton of CANTONS) {
      const title = `${svc.nom} ${canton.prep} ${canton.nom} — Val-Débarras`;
      const slug  = `${svc.slug}-${canton.slug}`;

      // Check if exists
      const existing = await wpGet(`canton_page?slug=${slug}&status=any`);
      if (existing.status === 200 && existing.body.length > 0) {
        console.log(`  ↷ Existe: ${title}`);
        skipped++;
        continue;
      }

      const result = await wpPost('canton_page', {
        title,
        slug,
        status: 'publish',
        content: buildContent(svc, canton),
        meta: {
          canton_nom:       canton.nom,
          canton_code:      canton.code,
          service_nom:      svc.nom,
          service_slug:     svc.slug,
          communes_pills:   canton.communes,
          hero_text:        `${svc.nom} ${canton.prep} ${canton.nom} — intervention rapide, devis gratuit sous 24h.`,
          meta_description: `${svc.nom} ${canton.prep} ${canton.nom} avec Val-Débarras. Devis gratuit, intervention rapide. ☎ 079 580 58 57`,
        },
      });

      if (result.status === 201) {
        console.log(`  ✓ Créé: ${title} (ID: ${result.body.id})`);
        created++;
      } else {
        console.error(`  ✗ Erreur (${result.status}): ${title} — ${JSON.stringify(result.body).substring(0, 100)}`);
        errors++;
      }

      // Small delay to avoid rate-limiting
      await new Promise(r => setTimeout(r, 300));
    }
  }

  console.log(`\n=== Résultat ===`);
  console.log(`  Créées : ${created}`);
  console.log(`  Ignorées (existantes) : ${skipped}`);
  console.log(`  Erreurs : ${errors}`);
  console.log(`\nÉtapes suivantes (à faire dans l'admin WP) :`);
  console.log(`  1. Importer CF7 form: cf7-forms/devis-form.json`);
  console.log(`  2. Importer champs ACF: acf-groups/canton-page-fields.json`);
  console.log(`  3. Uploader les images (images/*.jpg, images/*.svg)`);
  console.log(`  4. Configurer permalink: Réglages → Permaliens → /%postname%/`);
  console.log(`  5. Soumettre sitemap.xml à Google Search Console`);
}

main().catch(err => {
  console.error('Erreur fatale:', err);
  process.exit(1);
});
