@echo off
REM Script de démarrage pour le développement local (Windows)

echo 🚀 Démarrage de l'API AI News Paper en mode développement

REM Vérifier si .env existe
if not exist .env (
    echo ⚠️  Fichier .env non trouvé
    if exist .env.example (
        echo 📝 Création d'un fichier .env depuis .env.example...
        copy .env.example .env
        echo ✅ Fichier .env créé. Veuillez y ajouter votre OPENAI_API_KEY
        exit /b 1
    ) else (
        echo ❌ Fichier .env.example non trouvé
        exit /b 1
    )
)

REM Charger les variables d'environnement depuis .env
for /f "tokens=*" %%a in ('type .env ^| findstr /v "^#"') do set %%a

REM Vérifier que OPENAI_API_KEY est définie
if "%OPENAI_API_KEY%"=="" (
    echo ❌ OPENAI_API_KEY non définie dans .env
    exit /b 1
)

REM Créer les dossiers nécessaires
if not exist outputs mkdir outputs
if not exist static mkdir static

echo ✅ Configuration OK
echo 🌐 Démarrage du serveur sur http://localhost:8000
echo 📚 Documentation disponible sur http://localhost:8000/docs
echo.

REM Démarrer le serveur avec auto-reload
uvicorn api:app --reload --host 0.0.0.0 --port 8000

