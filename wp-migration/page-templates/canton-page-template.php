<?php
/**
 * Template Name: Page Canton — Val-Débarras
 * Template Post Type: canton_page, page
 *
 * Template pour les 36 pages canton (service × canton)
 * Utilise ACF pour les champs spécifiques par canton
 */

defined('ABSPATH') || exit;

// Champs ACF (ou meta WordPress si ACF non installé)
$canton_nom     = get_field('canton_nom')     ?: get_post_meta(get_the_ID(), 'canton_nom', true);
$canton_code    = get_field('canton_code')    ?: get_post_meta(get_the_ID(), 'canton_code', true);
$service_nom    = get_field('service_nom')    ?: get_post_meta(get_the_ID(), 'service_nom', true);
$service_slug   = get_field('service_slug')   ?: get_post_meta(get_the_ID(), 'service_slug', true);
$hero_text      = get_field('hero_text')      ?: get_the_excerpt();
$communes_pills = get_field('communes_pills') ?: ''; // texte séparé par virgules
$hero_image     = get_the_post_thumbnail_url(get_the_ID(), 'large')
                  ?: get_template_directory_uri() . '/images/vd-hero.jpg';

$cantons = [
    'ge' => ['nom' => 'Genève',    'slug' => 'geneve'],
    'vd' => ['nom' => 'Vaud',      'slug' => 'vaud'],
    'vs' => ['nom' => 'Valais',    'slug' => 'valais'],
    'fr' => ['nom' => 'Fribourg',  'slug' => 'fribourg'],
    'ne' => ['nom' => 'Neuchâtel', 'slug' => 'neuchatel'],
    'ju' => ['nom' => 'Jura',      'slug' => 'jura'],
];

$services = [
    'appartement' => ['nom' => 'Débarras appartement',       'slug' => 'debarras-appartement'],
    'maison'      => ['nom' => 'Débarras maison',            'slug' => 'debarras-maison'],
    'succession'  => ['nom' => 'Après décès / succession',   'slug' => 'debarras-apres-deces'],
    'ems'         => ['nom' => 'Débarras EMS',               'slug' => 'debarras-ems'],
    'diogene'     => ['nom' => 'Diogène & insalubre',        'slug' => 'debarras-insalubre-diogene'],
    'nettoyage'   => ['nom' => 'Nettoyage extrême',          'slug' => 'nettoyage-extreme'],
];

get_header();
?>
<main id="main">

<!-- BREADCRUMB -->
<nav class="breadcrumb" aria-label="Fil d'Ariane">
  <a href="/">Accueil</a>
  <span>›</span>
  <a href="/<?= esc_attr($service_slug) ?>/"><?= esc_html($services[$service_slug]['nom'] ?? $service_nom) ?></a>
  <span>›</span>
  <img src="<?= get_stylesheet_directory_uri() ?>/images/shield-<?= esc_attr($canton_code) ?>.svg"
       alt="<?= esc_attr($canton_nom) ?>" width="16" height="20">
  <strong><?= esc_html($canton_nom) ?></strong>
</nav>

<!-- HERO CANTON -->
<section class="hero-canton">
  <div class="hero-canton-inner">
    <div class="hero-canton-text">
      <h1><?= esc_html(get_the_title()) ?></h1>
      <p class="hero-canton-lead"><?= wp_kses_post($hero_text) ?></p>
      <div class="hero-canton-ctas">
        <a href="tel:+41795805857" class="btn-primary">
          📞 079 580 58 57
        </a>
        <a href="#devis" class="btn-secondary">
          Devis gratuit — 24h
        </a>
      </div>
    </div>
    <div class="hero-canton-img">
      <img src="<?= esc_url($hero_image) ?>"
           alt="<?= esc_attr($service_nom . ' ' . $canton_nom) ?>"
           loading="lazy">
    </div>
  </div>
</section>

<!-- COMMUNES PILLS -->
<?php if ($communes_pills) : ?>
<section class="communes-section">
  <div class="communes-inner">
    <h2>Zones d'intervention</h2>
    <div class="cpill-row">
      <?php foreach (array_map('trim', explode(',', $communes_pills)) as $commune) : ?>
        <span class="cpill"><?= esc_html($commune) ?></span>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>

<!-- CONTENU PRINCIPAL (éditeur WP) -->
<section class="canton-content">
  <div class="canton-content-inner">
    <div class="canton-main-text">
      <?php the_content(); ?>
    </div>

    <!-- SIDEBAR — Sélecteur canton -->
    <aside class="canton-sidebar">
      <div class="sidebar-card">
        <h3>Intervenir dans un autre canton</h3>
        <ul>
          <?php foreach ($cantons as $code => $info) : ?>
            <?php if ($code === $canton_code) : ?>
              <li class="sidebar-canton-current">
                <img src="<?= get_stylesheet_directory_uri() ?>/images/shield-<?= esc_attr($code) ?>.svg"
                     alt="" width="20" height="26" loading="lazy">
                <strong><?= esc_html($info['nom']) ?></strong>
              </li>
            <?php else : ?>
              <li>
                <a href="/<?= esc_attr($service_slug) ?>/<?= esc_attr($info['slug']) ?>/">
                  <img src="<?= get_stylesheet_directory_uri() ?>/images/shield-<?= esc_attr($code) ?>.svg"
                       alt="" width="20" height="26" loading="lazy">
                  <?= esc_html($info['nom']) ?>
                </a>
              </li>
            <?php endif; ?>
          <?php endforeach; ?>
        </ul>
      </div>

      <!-- FORMULAIRE CF7 -->
      <div class="sidebar-form">
        <h3>Demander un devis gratuit</h3>
        <?php
        // Remplacer 123 par l'ID réel du formulaire CF7 après import
        echo do_shortcode('[contact-form-7 id="123" title="Formulaire Devis Val-Débarras"]');
        ?>
      </div>
    </aside>
  </div>
</section>

<!-- AUTRES SERVICES -->
<section class="autres-services">
  <div class="autres-services-inner">
    <h2>Autres services à <?= esc_html($canton_nom) ?></h2>
    <div class="autres-services-grid">
      <?php foreach ($services as $svc_key => $svc) :
        if ($svc_key === ($service_slug ?? '')) continue; ?>
        <a href="/<?= esc_attr($svc['slug']) ?>/<?= esc_attr($cantons[$canton_code]['slug'] ?? '') ?>/"
           class="autres-svc-card">
          <?= esc_html($svc['nom']) ?>
        </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

</main>
<?php get_footer(); ?>
