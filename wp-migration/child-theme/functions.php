<?php
/**
 * Val-Débarras Child Theme — functions.php
 * Prêt pour migration depuis prototype statique Vercel
 */

defined('ABSPATH') || exit;

// ── 1. Enqueue styles ──────────────────────────────────────────────────────
add_action('wp_enqueue_scripts', function () {
    // Charger le thème parent
    wp_enqueue_style(
        'parent-style',
        get_template_directory_uri() . '/style.css'
    );
    // Charger le thème enfant
    wp_enqueue_style(
        'child-style',
        get_stylesheet_uri(),
        ['parent-style'],
        wp_get_theme()->get('Version')
    );
});

// ── 2. Support des features WordPress ─────────────────────────────────────
add_action('after_setup_theme', function () {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', ['search-form', 'comment-form', 'gallery', 'caption']);
    add_theme_support('custom-logo', [
        'height'      => 60,
        'width'       => 60,
        'flex-height' => true,
        'flex-width'  => true,
    ]);

    // Menus de navigation
    register_nav_menus([
        'primary'   => 'Menu principal (desktop)',
        'mobile'    => 'Menu mobile drawer',
        'footer'    => 'Menu footer',
    ]);
});

// ── 3. Custom Post Type : Pages Canton ────────────────────────────────────
add_action('init', function () {
    register_post_type('canton_page', [
        'labels' => [
            'name'          => 'Pages Canton',
            'singular_name' => 'Page Canton',
            'add_new_item'  => 'Ajouter une page canton',
            'edit_item'     => 'Modifier la page canton',
        ],
        'public'       => true,
        'has_archive'  => false,
        'show_in_rest' => true,
        'supports'     => ['title', 'editor', 'thumbnail', 'custom-fields', 'excerpt'],
        'rewrite'      => false, // URLs gérées manuellement ci-dessous
        'menu_icon'    => 'dashicons-location-alt',
        'menu_position'=> 5,
    ]);
});

// ── 4. Permaliens pour les pages canton ───────────────────────────────────
// Structure : /debarras-appartement/geneve/
// Correspond exactement aux URLs du prototype Vercel
add_action('init', function () {
    $services = [
        'debarras-appartement'       => 'appartement',
        'debarras-maison'            => 'maison',
        'debarras-apres-deces'       => 'succession',
        'debarras-ems'               => 'ems',
        'debarras-insalubre-diogene' => 'diogene',
        'nettoyage-extreme'          => 'nettoyage',
    ];
    $cantons = ['geneve', 'vaud', 'valais', 'fribourg', 'neuchatel', 'jura'];

    foreach ($services as $slug => $type) {
        foreach ($cantons as $canton) {
            add_rewrite_rule(
                "^{$slug}/{$canton}/?$",
                "index.php?post_type=canton_page&canton_service={$type}&canton_slug={$canton}",
                'top'
            );
        }
    }
    add_rewrite_tag('%canton_service%', '([^&]+)');
    add_rewrite_tag('%canton_slug%', '([^&]+)');
});

// ── 5. Champs ACF pour pages canton (si ACF installé) ─────────────────────
// Les champs sont aussi définis dans acf-groups/canton-page-fields.json
// Importer via ACF → Outils → Importer des groupes de champs

// ── 6. SEO — og:image par défaut ──────────────────────────────────────────
add_action('wp_head', function () {
    if (!is_singular()) return;
    global $post;
    $og_image = 'https://www.val-debarras.ch/wp-content/uploads/vd-hero.jpg';
    if (has_post_thumbnail($post->ID)) {
        $og_image = get_the_post_thumbnail_url($post->ID, 'large');
    }
    echo '<meta property="og:image" content="' . esc_url($og_image) . '">' . "\n";
    echo '<meta property="og:image:width" content="1200">' . "\n";
    echo '<meta property="og:image:height" content="630">' . "\n";
    echo '<meta property="og:site_name" content="Val-Débarras">' . "\n";
    echo '<meta property="og:locale" content="fr_CH">' . "\n";
}, 5);

// ── 7. Désactiver les fonctionnalités inutiles ────────────────────────────
remove_action('wp_head', 'wp_generator');           // Masquer version WP
remove_action('wp_head', 'wlwmanifest_link');
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wp_shortlink_wp_head');
add_filter('the_generator', '__return_empty_string'); // Sécurité

// ── 8. Limiter les révisions de posts ─────────────────────────────────────
add_filter('wp_revisions_to_keep', fn($num, $post) => 5, 10, 2);

// ── 9. Contact Form 7 — redirection après envoi ───────────────────────────
// Ajouter ici les hooks CF7 si nécessaire
add_action('wpcf7_mail_sent', function ($contact_form) {
    // Log les soumissions (optionnel)
    error_log('[Val-Débarras] Formulaire soumis: ' . $contact_form->title());
});
