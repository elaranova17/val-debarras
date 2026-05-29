#!/bin/bash
# Val-Débarras — Script de déploiement Vercel
# Exécuter depuis le dossier prototype/

echo "🚀 Déploiement Val-Débarras Prototype → Vercel"
echo "================================================"

# Vérifier si connecté
if ! vercel whoami &>/dev/null; then
  echo "⚠️  Token expiré. Connexion en cours..."
  vercel login
fi

echo "✅ Connecté. Déploiement en production..."
vercel --prod --yes

echo ""
echo "🌐 Prototype disponible sur:"
echo "   https://val-debarras-prototype.vercel.app"
echo "   https://val-debarras-prototype.vercel.app/brand"
