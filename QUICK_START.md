# ⚡ Quick Start - 5 minutes pour démarrer

## 🚀 Démarrage le plus rapide possible

### En local (2 minutes)

```bash
# 1️⃣ Copiez le fichier d'exemple
copy .env.example .env     # Windows
# OU
cp .env.example .env       # Linux/Mac

# 2️⃣ Éditez .env et ajoutez votre clé OpenAI
# OPENAI_API_KEY=sk-proj-VOTRE_CLE_ICI

# 3️⃣ Installez les dépendances
pip install -r requirements.txt

# 4️⃣ Lancez !
start_dev.bat              # Windows
# OU
./start_dev.sh             # Linux/Mac
```

**✅ C'est tout !** Ouvrez http://localhost:8000

---

### Sur Railway (5 minutes)

```bash
# 1️⃣ Commitez votre code
git add .
git commit -m "API FastAPI ready"
git push

# 2️⃣ Allez sur railway.app
# - New Project
# - Deploy from GitHub
# - Choisissez votre repo

# 3️⃣ Ajoutez la variable d'environnement
# Dans Variables :
# OPENAI_API_KEY = sk-proj-VOTRE_CLE

# 4️⃣ Generate Domain
```

**✅ Votre API est en ligne !**

---

## 🎯 Test rapide

### Via l'interface web
1. Ouvrez http://localhost:8000
2. Remplissez le formulaire
3. Cliquez sur "Lancer la recherche"

### Via l'API directement
```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"subject": "Test"}'
```

### Via Swagger (le plus simple)
http://localhost:8000/docs

---

## 📱 Endpoints essentiels

| Endpoint | Action |
|----------|--------|
| `GET /` | Interface web |
| `GET /docs` | Documentation interactive |
| `GET /health` | Vérifier l'état |
| `POST /research` | Créer une recherche |
| `GET /latest` | Dernière recherche |

---

## ⚠️ Troubleshooting express

### Erreur OPENAI_API_KEY
```bash
# Vérifiez votre .env
cat .env | grep OPENAI_API_KEY
```

### Port déjà utilisé
```bash
# Changez le port
export PORT=8001  # Linux/Mac
set PORT=8001     # Windows
```

### Module introuvable
```bash
# Réinstallez
pip install -r requirements.txt
```

---

## 📚 Plus d'infos

- **Guide complet** : `README.md`
- **Déploiement** : `DEPLOYMENT_GUIDE.md`
- **Changements** : `CHANGELOG.md`
- **Résumé** : `TRANSFORMATION_SUMMARY.md`

---

**C'est parti ! 🎉**

