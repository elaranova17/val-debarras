# Guide de migration — Val-Débarras Vercel → WordPress

## Ordre des étapes (SEO safe — Google ne voit aucune interruption)

---

### ÉTAPE 1 — Plugins à installer sur WP
Installer dans cet ordre :

1. **Contact Form 7** (gratuit) — formulaires de contact
2. **Advanced Custom Fields (ACF)** (gratuit) — champs personnalisés pour pages canton
3. **Yoast SEO** ou **Rank Math** — meta titles, descriptions, sitemap
4. **WP Rocket** ou **LiteSpeed Cache** — performance
5. **Wordfence** — sécurité
6. **(optionnel) CF7 to WP DB** — sauvegarde des leads en base de données

---

### ÉTAPE 2 — Thème enfant
1. Aller dans **Apparence → Thèmes → Ajouter**
2. Uploader le dossier `child-theme/` (zipper d'abord)
3. Activer le thème enfant

---

### ÉTAPE 3 — Importer les champs ACF
1. Aller dans **ACF → Outils → Importer des groupes de champs**
2. Importer le fichier `acf-groups/canton-page-fields.json`

---

### ÉTAPE 4 — Importer le formulaire CF7
1. Aller dans **Contact → Importer** (via plugin CF7 Import/Export)
2. Importer `cf7-forms/devis-form.json`
3. Noter l'ID du formulaire créé (ex: 247)
4. Dans `page-templates/canton-page-template.php`, remplacer `id="123"` par l'ID réel

---

### ÉTAPE 5 — Créer les 36 pages canton
Utiliser le CPT "canton_page" pour créer les 36 pages :

| Service | Canton | URL cible |
|---------|--------|-----------|
| debarras-appartement | geneve | /debarras-appartement/geneve/ |
| debarras-appartement | vaud | /debarras-appartement/vaud/ |
| ... | ... | ... |

**Astuce** : Copier-coller le contenu HTML des fichiers `.html` existants dans l'éditeur WP.
Le texte de chaque page est dans : `ge-appartement.html`, `vd-maison.html`, etc.

---

### ÉTAPE 6 — Vérifier les permaliens
1. Aller dans **Réglages → Permaliens**
2. Choisir : `/%postname%/`
3. Cliquer **Enregistrer** (régénère les règles de réécriture)

---

### ÉTAPE 7 — Uploader les images
Images à uploader dans la médiathèque WP :

- `images/vd-hero.jpg` → image principale Vaud
- `images/ge-hero.jpg` → image principale Genève
- `images/vs-hero.jpg` → Valais
- `images/ne-hero.jpg` → Neuchâtel
- `images/ju-hero.jpg` → Jura
- `images/fr-hero.jpg` → Fribourg
- `images/shield-ge.svg`, `shield-vd.svg`, etc. → blasons cantonaux
- `images/logo-icon.png`, `logo-cube.svg` → logo

---

### ÉTAPE 8 — Installer le sitemap.xml
1. Copier `sitemap.xml` à la racine du WP (`public_html/sitemap.xml`)
2. **OU** laisser Yoast/RankMath générer le sitemap automatiquement
3. Soumettre à Google Search Console : `https://www.val-debarras.ch/sitemap.xml`

---

### ÉTAPE 9 — Migration SEO (CRITIQUE)
Pour que Google ne perde aucun classement :

**A. Même structure d'URL** — les 36 pages canton doivent avoir exactement les mêmes URLs :
```
/debarras-appartement/geneve/   ✓
/debarras-maison/vaud/          ✓
```

**B. Balises meta identiques** — copier depuis les fichiers HTML :
- `<title>` → champ Yoast "SEO Title"
- `<meta name="description">` → champ Yoast "Meta Description"

**C. Ne pas supprimer le prototype Vercel** jusqu'à 4 semaines après la migration. Laisser Vercel en ligne le temps que Google indexe le WP.

**D. Soumettre les nouvelles URLs** dans Google Search Console → Inspection d'URL → Demander l'indexation (pour les 36 pages clés)

---

### ÉTAPE 10 — DNS (si migration de domaine)
Si `val-debarras.ch` pointe actuellement sur Vercel et doit pointer sur WP :
1. Dans le DNS du registrar, modifier le champ A/CNAME pour pointer sur l'IP du serveur WP
2. Propagation : 24-48h
3. Configurer SSL/HTTPS sur le serveur WP (Let's Encrypt gratuit)

---

## Checklist post-migration

- [ ] Toutes les 36 URLs canton retournent HTTP 200
- [ ] Le formulaire de contact envoie bien les emails
- [ ] Images chargées correctement
- [ ] Google Search Console — pas d'erreurs 404
- [ ] PageSpeed Insights — score > 80 sur mobile
- [ ] Test formulaire complet (nom, email, service, canton, message)
- [ ] Sitemap soumis à Google
- [ ] Meta descriptions OK sur 5 pages aléatoires
- [ ] Analytics configuré (GA4)
- [ ] Backup automatique configuré (Updraft Plus)
