<?php
/**
 * Val-Débarras — WPCode Snippet (versión final activa)
 * Nombre: VD Full Page Renderer
 * Snippet ID en WP: 29839
 * Ubicación: Run Everywhere
 *
 * QUÉ HACE:
 *  1. Registra _vd_html en la REST API → permite actualizar HTML via script JS
 *  2. En template_redirect, sirve _vd_html directamente (sin wrapper WP/Storefront)
 *     Método A: is_singular('page') — cuando WP identifica la página correctamente
 *     Método B: get_page_by_path() — bypass para URLs interceptadas por CPT canton_page
 *
 * NOTAS:
 *  - El child theme registra rewrite rules para CPT 'canton_page' con prioridad 'top'
 *    que interceptan URLs como /debarras-appartement/geneve/ antes de que WP las route
 *    a la página real. El Método B resuelve este problema buscando por path en la BD.
 */

defined('ABSPATH') || exit;

// 1. Registrar _vd_html en la REST API
add_action('init', function () {
    register_post_meta('page', '_vd_html', [
        'show_in_rest'  => true,
        'single'        => true,
        'type'          => 'string',
        'auth_callback' => function () {
            return current_user_can('edit_posts');
        },
    ]);
});

// 2. Servir HTML directo — funciona aunque rewrite rules de CPT intercepten la URL
add_action('template_redirect', function () {
    $page_id = 0;

    // Metodo A: WP identifico correctamente la pagina
    if ( is_singular('page') ) {
        $page_id = get_queried_object_id();
    }

    // Metodo B: Buscar por path en la BD (bypassa rewrite rules del CPT canton_page)
    if ( ! $page_id ) {
        $path = trim( parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ), '/' );
        $path = strtok( $path, '?' );
        $page = get_page_by_path( $path );
        if ( $page && $page->post_status === 'publish' ) {
            $page_id = $page->ID;
        }
    }

    if ( ! $page_id ) return;

    $html = get_post_meta( $page_id, '_vd_html', true );
    if ( ! $html ) return;

    // Inyectar fixes mobile/landscape antes de </head>
    $mobile_css = '<style>
/* ── Mobile landscape fixes v2 (WPCode) ── */
html,body{overflow-x:clip;max-width:100vw;}
@media(max-width:1024px){
  .header-inner{padding:0 12px !important;gap:8px !important;height:60px !important;}
  .header-cta,.header-phone,.desktop-only-phone{display:none !important;}
  .header-actions{display:flex !important;}
  .hamburger{display:flex !important;}
  .form-inner{grid-template-columns:1fr !important;gap:32px !important;}
  .form-section{padding:48px 0 !important;}
  .form-card{padding:24px 16px !important;}
}
@media(min-width:1025px){
  .header-actions{display:none !important;}
  .header-cta{display:flex !important;}
  .hamburger{display:none !important;}
  .nav{display:flex !important;}
  .header-inner{height:96px !important;padding:0 24px !important;}
}
</style>';
    $html = str_replace( '</head>', $mobile_css . '</head>', $html );

    status_header(200);
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Robots-Tag: index, follow');
    header('Cache-Control: public, max-age=3600');
    echo $html;
    exit;
}, 1);
