# Val-Débarras — Checklist Go-Live

> Todo listo. Cuando el cliente diga "go", seguir este orden exacto.
> Tiempo estimado: **30-45 minutos**

---

## PASO 1 — Plugins WordPress (5 min)

Instalar en `WP Admin → Extensions → Ajouter` si no están ya:

| Plugin | Gratis | Para qué |
|--------|--------|----------|
| **Contact Form 7** | ✓ | Formulario de cotización |
| **Advanced Custom Fields** | ✓ | Campos canton/service |
| **Yoast SEO** | ✓ | Meta titles, sitemap |
| **WP Rocket** o **LiteSpeed Cache** | ✓/Pago | Velocidad |
| **Wordfence** | ✓ | Seguridad |

---

## PASO 2 — Subir el Thème Enfant (3 min)

1. `Apparence → Thèmes → Ajouter → Uploader un thème`
2. Subir **`child-theme.zip`** (está en esta carpeta)
3. Activar el tema

---

## PASO 3 — Importar campos ACF (2 min)

1. `ACF → Outils → Importer des groupes de champs`
2. Subir **`acf-groups/canton-page-fields.json`**

---

## PASO 4 — Importar formulario CF7 (3 min)

1. Instalar plugin "CF7 Import & Export" si hace falta
2. `Contact → Importer`
3. Subir **`cf7-forms/devis-form.json`**
4. Anotar el ID del formulario creado (ej: 247)
5. En `page-templates/canton-page-template.php`, cambiar `id="123"` → `id="247"`

---

## PASO 5 — Crear las 36 páginas canton (10 min)

**Opción A — Desde tu portátil (recomendado):**
```bash
cd wp-migration
npm install
WP_USER=tu_usuario WP_PASS="3on3 nA38 tflT Qy2x A2xt a1TK" npm run import
```

**Opción B — Por SSH en el servidor:**
```bash
cd /ruta/wordpress
bash wp-migration/import-wp-cli.sh
```

---

## PASO 6 — Permaliens (1 min)

`Réglages → Permaliens → /%postname%/ → Enregistrer`

---

## PASO 7 — Imágenes (5 min)

`Médias → Ajouter` — subir todas las imágenes de la carpeta `images/`:

- `vd-hero.jpg`, `ge-hero.jpg`, `vs-hero.jpg`, `ne-hero.jpg`, `ju-hero.jpg`, `fr-hero.jpg`
- `shield-ge.svg`, `shield-vd.svg`, `shield-vs.svg`, `shield-fr.svg`, `shield-ne.svg`, `shield-ju.svg`
- `logo-icon.png`, `logo-cube.svg`

---

## PASO 8 — DNS (cuando estés listo para el cambio)

> ⚠️ Este paso hace que el dominio deje de apuntar a Vercel.
> Esperar confirmación del cliente antes de hacerlo.

1. En el registrar del dominio, cambiar el campo A/CNAME de `val-debarras.ch` para que apunte al IP del servidor WP
2. Propagación: 24-48h
3. Configurar SSL (Let's Encrypt, gratis)

---

## PASO 9 — Sitemap + Google Search Console (5 min)

1. Yoast genera el sitemap automáticamente en `/sitemap_index.xml`
2. Google Search Console → Sitemaps → Agregar `https://www.val-debarras.ch/sitemap_index.xml`

---

## Checklist de verificación post-go-live

- [ ] Las 36 URLs devuelven HTTP 200
- [ ] El formulario envía emails a `info@val-debarras.ch`
- [ ] Las imágenes cargan correctamente
- [ ] Google Search Console — sin errores 404
- [ ] PageSpeed Insights — score > 80 en mobile
- [ ] Meta descriptions OK en 5 páginas al azar
- [ ] Analytics GA4 configurado
- [ ] Backup automático configurado (UpdraftPlus)

---

## URLs críticas a verificar

```
/debarras-appartement/geneve/     ← más importante
/debarras-maison/vaud/
/debarras-apres-deces/geneve/
/nettoyage-extreme/vaud/
/debarras-ems/fribourg/
```

---

## Contacto urgente

**Teléfono:** 079 580 58 57  
**Email admin WP:** info@val-debarras.ch  
**Vercel (prototipo activo):** val-debarras-prototype.vercel.app  

> El prototipo Vercel se queda activo durante mínimo 4 semanas después del go-live,
> mientras Google indexa el nuevo WordPress.
