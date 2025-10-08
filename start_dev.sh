#!/bin/bash
# Script de démarrage pour le développement local

echo "🚀 Démarrage de l'API AI News Paper en mode développement"

# Vérifier si .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé"
    echo "📝 Création d'un fichier .env depuis .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Fichier .env créé. Veuillez y ajouter votre OPENAI_API_KEY"
        exit 1
    else
        echo "❌ Fichier .env.example non trouvé"
        exit 1
    fi
fi

# Charger les variables d'environnement
export $(cat .env | grep -v '^#' | xargs)

# Vérifier que OPENAI_API_KEY est définie
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY non définie dans .env"
    exit 1
fi

# Créer le dossier outputs s'il n'existe pas
mkdir -p outputs

# Créer le dossier static s'il n'existe pas
mkdir -p static

echo "✅ Configuration OK"
echo "🌐 Démarrage du serveur sur http://localhost:8000"
echo "📚 Documentation disponible sur http://localhost:8000/docs"
echo ""

# Démarrer le serveur avec auto-reload
uvicorn api:app --reload --host 0.0.0.0 --port 8000

