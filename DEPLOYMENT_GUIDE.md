# 🚀 Guide de Déploiement - AI News Paper API

Ce guide vous accompagne pas à pas pour déployer votre API FastAPI sur Railway.

## 📋 Table des matières

1. [Préparation](#préparation)
2. [Déploiement sur Railway](#déploiement-sur-railway)
3. [Test en local](#test-en-local)
4. [Déploiement avec Docker](#déploiement-avec-docker)
5. [Dépannage](#dépannage)

---

## Préparation

### 1. Obtenir une clé API OpenAI

1. Créez un compte sur [OpenAI Platform](https://platform.openai.com/)
2. Allez dans [API Keys](https://platform.openai.com/api-keys)
3. Cliquez sur "Create new secret key"
4. **Copiez et sauvegardez votre clé** (elle ne sera affichée qu'une fois)

### 2. Préparer votre dépôt Git

```bash
# Cloner ou créer votre dépôt
git init
git add .
git commit -m "Initial commit - API FastAPI"

# Pousser vers GitHub (ou GitLab, Bitbucket)
git remote add origin https://github.com/votre-username/votre-repo.git
git push -u origin main
```

**⚠️ Important** : Vérifiez que vous n'avez PAS committé de clé API !

```bash
# Vérifier qu'aucune clé n'est présente
git log -p | grep -i "sk-proj"
```

---

## Déploiement sur Railway

### Méthode 1 : Via l'interface web (Recommandé)

#### Étape 1 : Créer un projet

1. Allez sur [railway.app](https://railway.app/)
2. Connectez-vous (GitHub recommandé)
3. Cliquez sur **"New Project"**
4. Sélectionnez **"Deploy from GitHub repo"**
5. Choisissez votre dépôt `AiNp`

#### Étape 2 : Configurer les variables d'environnement

1. Dans votre projet Railway, cliquez sur l'onglet **"Variables"**
2. Ajoutez les variables suivantes :

```
OPENAI_API_KEY = sk-proj-VOTRE_CLE_ICI
PORT = 8000
```

Variables optionnelles (recommandées) :

```
OPENAI_MODEL = gpt-5
OPENAI_VERBOSITY = medium
OPENAI_REASONING_EFFORT = medium
```

#### Étape 3 : Déployer

1. Railway détectera automatiquement `railway.toml`
2. Le build démarre automatiquement
3. Attendez que le statut passe à **"Active"**
4. Cliquez sur **"Generate Domain"** pour obtenir une URL publique

#### Étape 4 : Vérifier le déploiement

1. Visitez `https://votre-app.up.railway.app/`
2. Vous devriez voir l'interface web
3. Testez `/health` : `https://votre-app.up.railway.app/health`
4. Accédez à la doc : `https://votre-app.up.railway.app/docs`

### Méthode 2 : Via Railway CLI

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Se connecter
railway login

# Initialiser le projet
railway init

# Définir les variables d'environnement
railway variables set OPENAI_API_KEY=sk-proj-VOTRE_CLE_ICI

# Déployer
railway up
```

---

## Test en local

### Méthode 1 : Scripts de démarrage (Plus simple)

#### Sur Linux/Mac :

```bash
chmod +x start_dev.sh
./start_dev.sh
```

#### Sur Windows :

```bash
start_dev.bat
```

### Méthode 2 : Manuel

```bash
# 1. Créer un environnement virtuel
python -m venv venv

# 2. Activer l'environnement
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer le fichier .env
cp .env.example .env
# Éditez .env et ajoutez votre OPENAI_API_KEY

# 5. Lancer le serveur
uvicorn api:app --reload --port 8000
```

### Accéder à l'API

- **Interface web** : http://localhost:8000/
- **Documentation Swagger** : http://localhost:8000/docs
- **Documentation ReDoc** : http://localhost:8000/redoc
- **Health check** : http://localhost:8000/health

### Tester avec le script Python

```bash
python test_api.py
```

---

## Déploiement avec Docker

### Build et run localement

```bash
# Build l'image
docker build -t ai-news-paper .

# Run le conteneur
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-proj-VOTRE_CLE_ICI \
  -v $(pwd)/outputs:/app/outputs \
  ai-news-paper
```

### Avec Docker Compose

```bash
# Créer le fichier .env
cp .env.example .env
# Éditez .env avec votre clé API

# Lancer
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

---

## Dépannage

### Erreur : "OPENAI_API_KEY non configurée"

**Solution** :
1. Vérifiez que la variable est bien définie dans Railway
2. Redéployez après avoir ajouté la variable
3. Vérifiez les logs : `railway logs`

### Erreur : "Module 'openai' not found"

**Solution** :
```bash
pip install -r requirements.txt
```

### Erreur : Port déjà utilisé

**Solution** :
```bash
# Changer le port
export PORT=8001
uvicorn api:app --port 8001
```

### L'API est lente

**Cause** : Les requêtes OpenAI avec Web Search peuvent prendre plusieurs minutes.

**Solutions** :
- Utilisez `reasoning_effort: "low"` pour des réponses plus rapides
- Consultez la section "Background Tasks" dans le code pour implémenter des tâches asynchrones

### Railway : Build échoue

**Vérifications** :
1. Tous les fichiers sont bien committés : `git status`
2. `requirements.txt` est présent et correct
3. `railway.toml` est présent
4. Vérifiez les logs de build dans Railway

### Erreur CORS lors des appels depuis un frontend

**Solution** : Ajoutez le middleware CORS dans `api.py` :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod, spécifiez vos domaines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Monitoring

### Sur Railway

1. **Logs en temps réel** : Dans le dashboard Railway
2. **Métriques** : CPU, RAM, Network
3. **Alertes** : Configurables dans les paramètres

### Logs de l'application

L'API utilise `print()` pour les logs. Consultez-les avec :

```bash
# Railway
railway logs

# Docker
docker-compose logs -f

# Local
# Les logs s'affichent dans le terminal
```

---

## 🔐 Sécurité pour la production

### 1. Ajouter de l'authentification

Exemple avec une clé API simple :

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_SECRET_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.post("/research", dependencies=[Depends(verify_api_key)])
async def create_research(...):
    ...
```

### 2. Rate limiting

Installez `slowapi` :

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/research")
@limiter.limit("5/minute")
async def create_research(request: Request, ...):
    ...
```

### 3. HTTPS

Railway fournit automatiquement HTTPS pour tous les domaines générés.

---

## 📈 Évolutions futures

### Fonctionnalités à ajouter

- [ ] Authentification utilisateur
- [ ] Webhook pour notifier la fin d'une recherche
- [ ] Support multi-langues
- [ ] Export en PDF/Markdown
- [ ] Base de données (PostgreSQL) au lieu de fichiers
- [ ] Cache Redis pour les requêtes fréquentes
- [ ] Queue de tâches (Celery/Redis) pour les recherches longues

### Optimisations

- [ ] Pagination pour `/list`
- [ ] Compression des réponses (gzip)
- [ ] CDN pour les fichiers statiques
- [ ] Background tasks pour les recherches

---

## 📚 Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Railway](https://docs.railway.app/)
- [Documentation OpenAI](https://platform.openai.com/docs)
- [Pydantic](https://docs.pydantic.dev/)

---

## 🆘 Support

Si vous rencontrez des problèmes :

1. Consultez les logs
2. Vérifiez la section [Dépannage](#dépannage)
3. Testez l'endpoint `/health`
4. Vérifiez que votre clé API OpenAI est valide

---

**Bon déploiement ! 🚀**

