# Changelog - Transformation en API FastAPI

## 🚀 Version 2.0.0 - API FastAPI (2025-10-08)

### ✨ Nouvelles fonctionnalités

#### API REST complète
- **Transformation complète en API FastAPI** avec endpoints RESTful
- **Interface web interactive** (`static/index.html`) pour tester l'API sans code
- **Documentation auto-générée** (Swagger UI et ReDoc)
- **Gestion multi-recherches** avec stockage des résultats

#### Endpoints disponibles
- `GET /` - Page d'accueil / Interface web
- `GET /health` - Vérification de l'état de l'API
- `POST /research` - Lancer une nouvelle recherche
- `GET /results/{research_id}` - Récupérer les résultats (JSON ou texte)
- `GET /latest` - Récupérer la dernière recherche
- `GET /list` - Lister toutes les recherches
- `DELETE /results/{research_id}` - Supprimer une recherche

#### Stockage et organisation
- **Stockage structuré** dans le dossier `outputs/`
- **ID uniques** (UUID) pour chaque recherche
- **Métadonnées complètes** sauvegardées en JSON
- **Multi-format** : export en JSON ou texte brut

### 🔧 Améliorations techniques

#### Sécurité
- ✅ **Clés API sécurisées** via variables d'environnement
- ✅ **`.gitignore` complet** pour éviter les fuites de secrets
- ✅ **Pas de clés hardcodées** dans le code
- ✅ **Vérification automatique** avec `check_config.py`

#### Configuration
- **Variables d'environnement** pour tous les paramètres
- **Configuration par requête** possible (model, verbosity, reasoning_effort)
- **Defaults intelligents** pour faciliter l'utilisation

#### Infrastructure
- **Railway.toml** pour déploiement automatique
- **Dockerfile** pour conteneurisation
- **Docker Compose** pour environnement local complet
- **Procfile** pour compatibilité multi-plateforme

### 📝 Documentation

#### Guides complets
- `README.md` - Documentation principale complète
- `DEPLOYMENT_GUIDE.md` - Guide de déploiement détaillé
- `CHANGELOG.md` - Historique des changements (ce fichier)

#### Scripts utilitaires
- `check_config.py` - Vérification de la configuration avant déploiement
- `test_api.py` - Script de test automatisé de l'API
- `start_dev.sh` / `start_dev.bat` - Démarrage rapide en local

### 🎨 Interface utilisateur

#### Interface web moderne
- Design responsive et moderne
- Formulaire de recherche complet
- Affichage des recherches récentes
- Visualisation des résultats
- Indicateur de santé de l'API

### 🐳 Containerisation

#### Docker
- `Dockerfile` optimisé pour production
- `docker-compose.yml` pour développement local
- `.dockerignore` pour images légères

### 📦 Dépendances ajoutées

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
python-multipart>=0.0.6
```

### 🔄 Migration depuis la version CLI

#### Avant (v1.0.0)
```bash
# Script CLI simple
python main.py
# Résultats dans output.txt et metadata.json
```

#### Maintenant (v2.0.0)
```bash
# API REST complète
uvicorn api:app --reload

# Puis utilisation via HTTP
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"subject": "Mon sujet"}'
```

#### Rétrocompatibilité
Le script CLI original (`main.py`) est conservé pour compatibilité.

### 🚀 Déploiement

#### Railway
- Configuration automatique via `railway.toml`
- HTTPS automatique
- Variables d'environnement sécurisées
- Logs en temps réel

#### Local
Plusieurs méthodes disponibles :
1. Scripts de démarrage (`start_dev.sh` / `start_dev.bat`)
2. Commande directe (`uvicorn api:app --reload`)
3. Docker Compose (`docker-compose up`)

### 📊 Comparaison

| Fonctionnalité | v1.0.0 (CLI) | v2.0.0 (API) |
|----------------|--------------|--------------|
| Mode d'utilisation | Script CLI | API REST |
| Interface | Terminal | Web + API |
| Multi-utilisateurs | ❌ | ✅ |
| Historique | 1 seul résultat | Illimité |
| Documentation | README | README + Swagger + ReDoc |
| Déploiement | ❌ | Railway, Docker |
| Sécurité | Clé hardcodée | Variables d'env |
| Tests | ❌ | Script inclus |

### 🎯 Cas d'usage

#### Avant (CLI)
- Recherche ponctuelle en local
- Usage personnel

#### Maintenant (API)
- Service web hébergé
- Intégration dans d'autres applications
- Usage partagé en équipe
- Automatisation via webhooks
- Interface web accessible partout

### ⚙️ Configuration

#### Variables d'environnement supportées
```env
OPENAI_API_KEY           # Requis
PORT                     # Optionnel (défaut: 8000)
OPENAI_MODEL            # Optionnel (défaut: gpt-5)
OPENAI_VERBOSITY        # Optionnel (défaut: medium)
OPENAI_REASONING_EFFORT # Optionnel (défaut: medium)
```

### 🧪 Tests

#### Script de test automatisé
```bash
python test_api.py
```

Tests inclus :
- ✅ Health check
- ✅ Création de recherche
- ✅ Récupération des résultats
- ✅ Listing des recherches
- ✅ Dernière recherche

### 📈 Performances

#### Améliorations
- Stockage des résultats pour consultation rapide
- Pas de re-calcul pour les recherches passées
- Support du cache navigateur pour l'interface web

#### À venir
- [ ] Queue de tâches pour recherches en arrière-plan
- [ ] Cache Redis pour recherches fréquentes
- [ ] Rate limiting pour éviter les abus

### 🔮 Roadmap future

#### Version 2.1.0 (Prévue)
- [ ] Authentification utilisateur
- [ ] Webhooks pour notifications
- [ ] Export PDF/Markdown
- [ ] Base de données PostgreSQL

#### Version 2.2.0 (Prévue)
- [ ] Background tasks (Celery)
- [ ] Support multi-langues
- [ ] Templates personnalisables
- [ ] Analytics et statistiques

### 🐛 Corrections

- ✅ Clé API n'est plus exposée dans le code
- ✅ Fichier .gitignore complet
- ✅ Gestion propre des erreurs
- ✅ Validation des entrées avec Pydantic

### 💡 Notes de migration

Pour migrer du script CLI vers l'API :

1. **Installer les nouvelles dépendances**
   ```bash
   pip install -r requirements.txt
   ```

2. **Créer le fichier .env**
   ```bash
   cp .env.example .env
   # Éditer .env avec votre clé API
   ```

3. **Lancer l'API**
   ```bash
   ./start_dev.sh  # ou start_dev.bat sur Windows
   ```

4. **Accéder à l'interface**
   Ouvrir http://localhost:8000

### 🙏 Remerciements

Cette transformation en API FastAPI permet :
- ✅ Un déploiement facile sur Railway
- ✅ Une utilisation partagée
- ✅ Une meilleure sécurité
- ✅ Une interface web intuitive
- ✅ Une documentation automatique

---

## 📝 Version 1.0.0 - Script CLI initial

### Fonctionnalités
- Script Python CLI pour veille technologique
- Utilisation de l'API OpenAI avec Web Search
- Sauvegarde dans `output.txt` et `metadata.json`
- Configuration hardcodée

### Limitations
- Clé API hardcodée (non sécurisé)
- Pas de déploiement possible
- Usage local uniquement
- Un seul résultat à la fois

---

**Note** : Le script CLI original (`main.py`) reste disponible pour usage local simple.

