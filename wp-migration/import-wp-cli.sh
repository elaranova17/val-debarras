#!/bin/bash
# =============================================================================
# Val-Débarras — Script d'import automatisé via WP-CLI
# Exécuter sur le serveur WordPress (ou via SSH)
# Usage: bash import-wp-cli.sh
# =============================================================================

set -e

WP="wp --allow-root"
SITE_URL="https://www.val-debarras.ch"
ADMIN_EMAIL="info@val-debarras.ch"

echo "=== Val-Débarras WP-CLI Import ==="
echo "Site: $SITE_URL"
echo ""

# ── 1. Activer le thème enfant ───────────────────────────────────────────────
echo "[1/6] Activation du thème enfant..."
# Vérifier si le thème est installé
if $WP theme is-installed val-debarras-child 2>/dev/null; then
  $WP theme activate val-debarras-child
  echo "    ✓ Thème enfant activé"
else
  echo "    ⚠ Thème enfant pas installé — uploader d'abord le dossier child-theme/"
  echo "      via Apparence → Thèmes → Ajouter → Uploader"
fi

# ── 2. Flusher les règles de réécriture ─────────────────────────────────────
echo "[2/6] Flush des règles de réécriture..."
$WP rewrite flush
$WP rewrite structure '/%postname%/'
echo "    ✓ Permaliens configurés"

# ── 3. Créer les 36 pages canton ────────────────────────────────────────────
echo "[3/6] Création des 36 pages canton..."

declare -A SERVICES
SERVICES["debarras-appartement"]="Débarras appartement"
SERVICES["debarras-maison"]="Débarras maison"
SERVICES["debarras-apres-deces"]="Après décès / succession"
SERVICES["debarras-ems"]="Débarras EMS"
SERVICES["debarras-insalubre-diogene"]="Diogène & insalubre"
SERVICES["nettoyage-extreme"]="Nettoyage extrême"

declare -A CANTONS
CANTONS["geneve"]="Genève"
CANTONS["vaud"]="Vaud"
CANTONS["valais"]="Valais"
CANTONS["fribourg"]="Fribourg"
CANTONS["neuchatel"]="Neuchâtel"
CANTONS["jura"]="Jura"

declare -A CANTON_CODES
CANTON_CODES["geneve"]="ge"
CANTON_CODES["vaud"]="vd"
CANTON_CODES["valais"]="vs"
CANTON_CODES["fribourg"]="fr"
CANTON_CODES["neuchatel"]="ne"
CANTON_CODES["jura"]="ju"

declare -A COMMUNES
COMMUNES["geneve"]="Genève, Carouge, Lancy, Vernier, Meyrin, Onex, Thônex, Plan-les-Ouates, Bernex, Chêne-Bougeries"
COMMUNES["vaud"]="Lausanne, Morges, Nyon, Yverdon-les-Bains, Renens, Prilly, Pully, Gland, Rolle, Aigle"
COMMUNES["valais"]="Sion, Sierre, Martigny, Monthey, Visp, Brig, Naters, Leuk, Saas-Fee, Verbier"
COMMUNES["fribourg"]="Fribourg, Bulle, Romont, Murten, Estavayer-le-Lac, Châtel-Saint-Denis, Villars-sur-Glâne"
COMMUNES["neuchatel"]="Neuchâtel, La Chaux-de-Fonds, Le Locle, Boudry, Fleurier, Couvet, Peseux, Colombier"
COMMUNES["jura"]="Delémont, Porrentruy, Saignelégier, Bassecourt, Courrendlin, Courfaivre, Moutier"

CREATED=0
SKIPPED=0

for SVC_SLUG in "${!SERVICES[@]}"; do
  SVC_NOM="${SERVICES[$SVC_SLUG]}"

  for CANTON_SLUG in "${!CANTONS[@]}"; do
    CANTON_NOM="${CANTONS[$CANTON_SLUG]}"
    CANTON_CODE="${CANTON_CODES[$CANTON_SLUG]}"
    COMMUNES_LIST="${COMMUNES[$CANTON_SLUG]}"

    # Construire le titre de page
    case "$CANTON_SLUG" in
      geneve|neuchatel|fribourg) PREP="à" ;;
      vaud) PREP="dans le" ;;
      valais) PREP="en" ;;
      jura) PREP="au" ;;
    esac

    TITLE="${SVC_NOM} ${PREP} ${CANTON_NOM} — Val-Débarras"
    PAGE_SLUG="${SVC_SLUG}-${CANTON_SLUG}"

    # Vérifier si la page existe déjà
    EXISTING=$($WP post list --post_type=canton_page --post_status=any --name="${PAGE_SLUG}" --field=ID 2>/dev/null | head -1)

    if [ -n "$EXISTING" ]; then
      echo "    ↷ Existe déjà: $TITLE (ID: $EXISTING)"
      SKIPPED=$((SKIPPED + 1))
      continue
    fi

    # Contenu principal de la page
    CONTENT="<h2>${SVC_NOM} ${PREP} ${CANTON_NOM}</h2>
<p>Val-Débarras est votre spécialiste du ${SVC_NOM,,} ${PREP} ${CANTON_NOM} et dans toute la région. Notre équipe expérimentée intervient rapidement, avec professionnalisme et discrétion.</p>
<h3>Pourquoi choisir Val-Débarras ?</h3>
<ul>
<li>Intervention rapide — délai garanti sous 48h</li>
<li>Équipe professionnelle et discrète</li>
<li>Devis gratuit et sans engagement</li>
<li>Rachat du mobilier possible</li>
<li>Don aux associations caritatives (Caritas, Émmaüs)</li>
<li>Evacuation des déchets conforme aux normes suisses</li>
</ul>
<h3>Notre zone d'intervention ${PREP} ${CANTON_NOM}</h3>
<p>Nous intervenons dans tout le canton de ${CANTON_NOM} : ${COMMUNES_LIST}.</p>
<h3>FAQ — ${SVC_NOM} ${PREP} ${CANTON_NOM}</h3>
<p><strong>Quel est le prix d'un ${SVC_NOM,,} ${PREP} ${CANTON_NOM} ?</strong><br>
Le prix dépend du volume, de l'accessibilité et de l'urgence. Contactez-nous pour un devis gratuit.</p>
<p><strong>Combien de temps dure l'intervention ?</strong><br>
En général 1 à 3 jours selon la taille du logement. Nous vous donnons une estimation précise lors du devis.</p>"

    # Créer le post
    POST_ID=$($WP post create \
      --post_type=canton_page \
      --post_status=publish \
      --post_title="$TITLE" \
      --post_name="$PAGE_SLUG" \
      --post_content="$CONTENT" \
      --porcelain 2>/dev/null)

    if [ -n "$POST_ID" ]; then
      # Ajouter les meta fields
      $WP post meta update "$POST_ID" canton_nom "$CANTON_NOM"
      $WP post meta update "$POST_ID" canton_code "$CANTON_CODE"
      $WP post meta update "$POST_ID" service_nom "$SVC_NOM"
      $WP post meta update "$POST_ID" service_slug "$SVC_SLUG"
      $WP post meta update "$POST_ID" communes_pills "$COMMUNES_LIST"
      $WP post meta update "$POST_ID" hero_text "${SVC_NOM} ${PREP} ${CANTON_NOM} — intervention rapide, devis gratuit sous 24h."
      $WP post meta update "$POST_ID" meta_description "${SVC_NOM} ${PREP} ${CANTON_NOM} avec Val-Débarras. Devis gratuit, intervention rapide. ☎ 079 580 58 57"

      echo "    ✓ Créé: $TITLE (ID: $POST_ID)"
      CREATED=$((CREATED + 1))
    else
      echo "    ✗ Échec: $TITLE"
    fi
  done
done

echo ""
echo "    Pages créées: $CREATED | Ignorées (existantes): $SKIPPED"

# ── 4. Configurer les règles de réécriture pour les pages canton ─────────────
echo ""
echo "[4/6] Configuration des règles de réécriture..."
$WP rewrite flush --hard
echo "    ✓ Règles flushées"

# ── 5. Vérifier les URLs ─────────────────────────────────────────────────────
echo ""
echo "[5/6] Vérification des URLs (échantillon)..."
TEST_URLS=(
  "/debarras-appartement/geneve/"
  "/debarras-maison/vaud/"
  "/debarras-apres-deces/valais/"
  "/nettoyage-extreme/fribourg/"
)

for URL in "${TEST_URLS[@]}"; do
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${SITE_URL}${URL}")
  if [ "$HTTP_CODE" = "200" ]; then
    echo "    ✓ ${URL} → HTTP $HTTP_CODE"
  else
    echo "    ✗ ${URL} → HTTP $HTTP_CODE"
  fi
done

# ── 6. Générer le sitemap (si pas Yoast/RankMath) ───────────────────────────
echo ""
echo "[6/6] Sitemap..."
if $WP plugin is-active wordpress-seo 2>/dev/null || $WP plugin is-active seo-by-rank-math 2>/dev/null; then
  echo "    ✓ Sitemap géré par Yoast/RankMath"
else
  echo "    ⚠ Copier sitemap.xml à la racine du site (voir GUIDE-MIGRATION.md étape 8)"
fi

echo ""
echo "=== Import terminé ==="
echo ""
echo "Étapes manuelles restantes :"
echo "  1. Uploader le thème enfant (child-theme/) via l'admin WP si pas fait"
echo "  2. Importer le formulaire CF7 (cf7-forms/devis-form.json)"
echo "  3. Importer les champs ACF (acf-groups/canton-page-fields.json)"
echo "  4. Uploader les images dans la médiathèque"
echo "  5. Soumettre le sitemap à Google Search Console"
