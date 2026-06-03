# Procédure de migration — Val-Débarras → WordPress
## Préserver le Quality Score Google Ads via 301 propres

---

## Structure des URLs cibles

```
https://www.val-debarras.ch/                              ← homepage
https://www.val-debarras.ch/debarras-appartement/        ← page générique (nouvelle)
https://www.val-debarras.ch/debarras-appartement/geneve/ ← page canton
https://www.val-debarras.ch/debarras-appartement/geneve/merci/ ← conversion Google Ads
```

### Services (6)
| Slug WP | Service |
|---------|---------|
| `debarras-appartement` | Débarras appartement |
| `debarras-maison` | Débarras maison |
| `debarras-apres-deces-succession` | Après décès / succession |
| `debarras-ems` | Débarras EMS |
| `debarras-insalubre-diogene` | Diogène & insalubre |
| `nettoyage-extreme` | Nettoyage extrême |

### Cantons (6)
`geneve` · `vaud` · `valais` · `fribourg` · `neuchatel` · `jura`

**Total : 6 pages génériques + 36 pages canton + 36 pages merci = 78 pages**

---

## PHASE 1 — Préparer WordPress (sans couper le trafic)

### 1.1 Permaliens
```
WP Admin → Réglages → Permaliens → /%postname%/ → Enregistrer
```
⚠️ OBLIGATOIRE avant l'import, sinon les URLs seront en `?p=123`

### 1.2 Installer les plugins requis
- **Contact Form 7** (formulaire devis)
- **Redirection** (301 redirects, auteur John Godley)
- **Yoast SEO** (meta descriptions, noindex sur pages merci)

### 1.3 Activer le thème enfant
```
WP Admin → Apparence → Thèmes → Activer "Val-Débarras Child"
```
Fichiers dans `child-theme/` de ce repo.

### 1.4 Importer le formulaire CF7
```
WP Admin → Contact → Import → cf7-forms/devis-form.json
```
Dans les paramètres du formulaire CF7 → onglet "Message" :
- Redirection après envoi : activer "On Sent OK" → URL de redirection :
  `[valdebarras_merci_url]` (shortcode custom à ajouter dans functions.php)

---

## PHASE 2 — Importer les pages

Exécuter depuis votre machine locale (pas depuis le cloud) :

```bash
cd wp-migration
npm install node-fetch@2
WP_USER=votre_username WP_PASS="3on3 nA38 tflT Qy2x A2xt a1TK" node import-rest-api.js
```

Le script crée :
- 6 pages génériques service (parent)
- 36 pages canton (enfants des services)
- 36 pages merci (enfants des cantons, noindex)

**Idempotent** : peut être relancé sans risque.

---

## PHASE 3 — Configurer les redirects 301

### 3.1 Plugin Redirection
```
WP Admin → Outils → Redirection → Import/Export → Import CSV
```
Importer : `wp-migration/redirects-plugin.csv`

Ceci gère les anciennes URLs WP (si elles existaient) vers les nouvelles.

### 3.2 Vérifier les redirects
```bash
node verify-urls.js
```
Toutes les URLs doivent retourner 200.

---

## PHASE 4 — Vérification avant bascule

### Checklist technique
- [ ] Toutes les 78 URLs retournent 200 (`node verify-urls.js`)
- [ ] Les formulaires CF7 envoient l'email ET redirigent vers /merci/
- [ ] Les pages merci affichent le tracking Google Ads (AW-XXXXXXXXXX)
- [ ] Yoast : pages merci en noindex, pages canton avec meta description
- [ ] Mobile : tester sur iPhone (Safari) et Android (Chrome)
- [ ] Vitesse : PageSpeed Insights > 70 sur mobile

---

## PHASE 5 — Mise à jour Google Ads (CRITIQUE)

⚠️ À faire IMMÉDIATEMENT après que WP est en ligne et testé.

### Nouvelles URLs finales à mettre dans Google Ads

| Ancien prototype | Nouvelle URL WP |
|-----------------|----------------|
| `val-debarras-prototype.vercel.app/ge-appartement` | `www.val-debarras.ch/debarras-appartement/geneve/` |
| `val-debarras-prototype.vercel.app/vd-appartement` | `www.val-debarras.ch/debarras-appartement/vaud/` |
| *(etc. pour les 36 pages canton)* | |

### Dans Google Ads :
1. Aller dans **Campagnes → Annonces**
2. Pour chaque annonce : modifier **"URL finale"** → nouvelle URL WP
3. Pour les extensions de liens annexes : idem
4. **Ne pas** changer les URLs une par une — utiliser l'**éditeur Google Ads** (export CSV → modifier → reimport)

### URLs de conversion Google Ads (pages merci)
Remplacer `AW-XXXXXXXXXX/YYYYYYYYYYYYYYYY` dans le tag gtag par les vrais IDs du client.
Ces IDs se trouvent dans : **Google Ads → Outils → Conversions → [nom conversion] → Tag**

---

## PHASE 6 — Bascule DNS (le jour J)

Si l'hébergement change également :
1. Baisser le TTL DNS à 300s (5 min) **48h avant** la bascule
2. Faire la bascule DNS un mardi ou mercredi matin (trafic faible)
3. Garder l'ancien serveur actif 48h après la bascule (les DNS propagent lentement)
4. Vérifier avec `curl -I https://www.val-debarras.ch/debarras-appartement/geneve/`

---

## PHASE 7 — Post-migration (J+1 à J+7)

- [ ] Google Search Console → Inspecter URL → demander indexation des 42 URLs principales
- [ ] Surveiller les erreurs 404 dans Search Console pendant 7 jours
- [ ] Vérifier que le Quality Score Google Ads ne baisse pas (surveiller 7 jours)
- [ ] Si QS baisse : vérifier que les pages merci se chargent rapidement et que le gtag est présent

---

## Notes importantes sur le Quality Score

Le QS Google Ads est lié à **3 facteurs** :
1. **Pertinence de l'annonce** → ne change pas
2. **Taux de clics attendu** → ne change pas
3. **Expérience de la page de destination** → peut varier 2-3 semaines post-migration

Les 301 redirects transmettent ~90% du "link juice" mais Google Ads réévalue quand même la page.
La meilleure protection : **mettre à jour les URLs finales dans les annonces** le plus vite possible
après que WP est live, plutôt que de laisser Google Ads suivre les redirections.
