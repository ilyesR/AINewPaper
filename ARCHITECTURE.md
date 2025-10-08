# 🏗️ Architecture de l'API

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                         UTILISATEUR                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │                                         │
        │  Interface Web (static/index.html)      │
        │  ou                                     │
        │  Client HTTP (curl, Python, etc.)       │
        │                                         │
        └─────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API FastAPI (api.py)                    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   GET /      │  │ GET /health  │  │ GET /docs    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │POST /research│  │ GET /results │  │ GET /latest  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  GET /list   │  │ DELETE /... │                         │
│  └──────────────┘  └──────────────┘                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenAI API Client                         │
│                                                              │
│  - GPT-5 (ou autre modèle)                                  │
│  - Web Search Tool                                          │
│  - Reasoning & Test-time compute                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │          Stockage Local (outputs/)      │
        │                                         │
        │  - {id}_output.txt                      │
        │  - {id}_metadata.json                   │
        │                                         │
        └─────────────────────────────────────────┘
```

## Flux de données

### 1. Création d'une recherche (POST /research)

```
┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│  Client  │─────▶│   API    │─────▶│  OpenAI  │─────▶│ Stockage │
└──────────┘      └──────────┘      └──────────┘      └──────────┘
     │                 │                  │                  │
     │ 1. POST        │ 2. Appel API    │ 3. Web Search   │
     │ /research      │                  │ + Reasoning     │
     │                │                  │                 │
     │                │ 4. Réponse      │ 5. Sauvegarde   │
     │ ◀──────────────│ ◀────────────────│ ◀───────────────│
     │ 6. research_id │                  │                 │
     │                │                  │                 │
```

### 2. Récupération d'un résultat (GET /results/{id})

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Client  │─────▶│   API    │─────▶│ Stockage │
└──────────┘      └──────────┘      └──────────┘
     │                 │                  │
     │ 1. GET         │ 2. Lecture       │
     │ /results/id    │                  │
     │                │                  │
     │                │ 3. Données       │
     │ ◀──────────────│ ◀────────────────│
     │ 4. JSON/Text   │                  │
     │                │                  │
```

## Structure des fichiers

```
api.py (Application principale)
│
├── Configuration
│   ├── API_KEY (depuis env)
│   ├── OUTPUT_DIR
│   ├── MODEL
│   ├── VERBOSITY
│   └── REASONING_EFFORT
│
├── Modèles Pydantic
│   ├── ResearchRequest
│   └── ResearchResponse
│
├── Fonction principale
│   └── perform_research()
│       ├── Créer client OpenAI
│       ├── Préparer les messages
│       ├── Appeler l'API
│       ├── Extraire la réponse
│       └── Sauvegarder les résultats
│
└── Endpoints FastAPI
    ├── GET  /              → root()
    ├── GET  /health        → health_check()
    ├── POST /research      → create_research()
    ├── GET  /results/{id}  → get_results()
    ├── GET  /latest        → get_latest()
    ├── GET  /list          → list_researches()
    └── DELETE /results/{id} → delete_research()
```

## Stack technique

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
├─────────────────────────────────────────────────────────────┤
│  - HTML5 + CSS3 + JavaScript Vanilla                        │
│  - Fetch API pour les requêtes HTTP                        │
│  - Interface responsive                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        Backend                               │
├─────────────────────────────────────────────────────────────┤
│  - FastAPI 0.104+       (Framework web)                     │
│  - Uvicorn              (Serveur ASGI)                      │
│  - Pydantic 2.0+        (Validation de données)             │
│  - Python 3.11          (Runtime)                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Services externes                         │
├─────────────────────────────────────────────────────────────┤
│  - OpenAI API           (IA générative)                     │
│  - Web Search Tool      (Recherche web)                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      Stockage                                │
├─────────────────────────────────────────────────────────────┤
│  - Système de fichiers  (outputs/*.txt, *.json)             │
│  - UUID pour identifiants uniques                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure                            │
├─────────────────────────────────────────────────────────────┤
│  - Railway.app          (Hébergement)                       │
│  - Docker               (Conteneurisation - optionnel)      │
│  - Git/GitHub           (Versioning)                        │
└─────────────────────────────────────────────────────────────┘
```

## Variables d'environnement

```
Environment Variables
│
├── OPENAI_API_KEY              [REQUIS]
│   └── Clé d'authentification OpenAI
│
├── PORT                        [OPTIONNEL - défaut: 8000]
│   └── Port d'écoute du serveur
│
├── OPENAI_MODEL                [OPTIONNEL - défaut: gpt-5]
│   └── Modèle OpenAI à utiliser
│
├── OPENAI_VERBOSITY            [OPTIONNEL - défaut: medium]
│   └── Niveau de détail (low/medium/high)
│
└── OPENAI_REASONING_EFFORT     [OPTIONNEL - défaut: medium]
    └── Effort de raisonnement (low/medium/high)
```

## Cycle de vie d'une recherche

```
1. CRÉATION
   ├── Génération UUID
   ├── Validation des données (Pydantic)
   └── État: pending

2. TRAITEMENT
   ├── Appel OpenAI API
   ├── Web Search (si nécessaire)
   ├── Raisonnement
   └── État: in_progress

3. SAUVEGARDE
   ├── Création fichier output.txt
   ├── Création fichier metadata.json
   └── État: completed

4. RÉCUPÉRATION
   ├── Lecture depuis outputs/
   └── Retour JSON ou texte

5. SUPPRESSION (optionnel)
   ├── Suppression fichiers
   └── État: deleted
```

## Sécurité

```
┌─────────────────────────────────────────────────────────────┐
│                    Couches de sécurité                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Variables d'environnement                               │
│     └── Clés API non hardcodées                            │
│                                                              │
│  2. .gitignore                                              │
│     └── Secrets non versionnés                             │
│                                                              │
│  3. Validation Pydantic                                     │
│     └── Données validées                                    │
│                                                              │
│  4. HTTPS (Railway)                                         │
│     └── Communication chiffrée                              │
│                                                              │
│  5. [À ajouter] Authentification                            │
│     └── API Keys / JWT                                      │
│                                                              │
│  6. [À ajouter] Rate Limiting                               │
│     └── Protection contre abus                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Scalabilité

### Actuel (MVP)

```
Single Instance
│
├── Stockage: Fichiers locaux
├── Concurrence: Limitée par l'instance
└── État: Stateful (fichiers)
```

### Évolution possible (Future)

```
Multiple Instances
│
├── Stockage: Base de données (PostgreSQL)
│   └── Recherches persistantes
│
├── Cache: Redis
│   └── Résultats fréquents
│
├── Queue: Celery + Redis
│   └── Traitements asynchrones
│
├── Load Balancer
│   └── Distribution de charge
│
└── État: Stateless (scale horizontal)
```

## Monitoring et logs

```
Application Logs
│
├── Print statements
│   └── Logs console
│
├── Railway Logs
│   └── Logs centralisés
│
├── [À ajouter] Structured logging
│   └── JSON logs
│
└── [À ajouter] Monitoring
    ├── Métriques (Prometheus)
    ├── Tracing (Jaeger)
    └── Alertes (PagerDuty)
```

## Points d'extension

### 1. Authentification
```python
from fastapi import Depends, HTTPException, Header

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_SECRET:
        raise HTTPException(403)
    return x_api_key

@app.post("/research", dependencies=[Depends(verify_api_key)])
```

### 2. Base de données
```python
from sqlalchemy import create_engine
from databases import Database

database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()
```

### 3. Background tasks
```python
from fastapi import BackgroundTasks

@app.post("/research")
async def create_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks
):
    research_id = generate_id()
    background_tasks.add_task(perform_research, ...)
    return {"research_id": research_id, "status": "pending"}
```

### 4. Webhooks
```python
async def notify_completion(webhook_url: str, data: dict):
    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, json=data)
```

## Performances

### Temps de réponse typiques

```
┌──────────────────┬─────────────────┬───────────────┐
│    Endpoint      │   Temps moyen   │   Cacheable   │
├──────────────────┼─────────────────┼───────────────┤
│ GET /health      │     < 10ms      │      ✅       │
│ GET /list        │     < 50ms      │      ✅       │
│ GET /results     │     < 100ms     │      ✅       │
│ POST /research   │   2-10 minutes  │      ❌       │
└──────────────────┴─────────────────┴───────────────┘
```

### Optimisations possibles

1. **Cache des résultats** (Redis)
2. **Compression** (gzip)
3. **CDN** pour fichiers statiques
4. **Database indexes**
5. **Connection pooling**

---

## 🔗 Diagrammes de séquence

### Requête simple (GET /health)

```
Client          API
  │              │
  │─────GET─────▶│
  │  /health     │
  │              │
  │◀────200─────│
  │   { ... }    │
  │              │
```

### Requête complexe (POST /research)

```
Client      API         OpenAI      Stockage
  │          │            │            │
  │──POST───▶│            │            │
  │/research │            │            │
  │          │            │            │
  │          │───Call────▶│            │
  │          │  API       │            │
  │          │            │            │
  │          │            │──Search───▶│
  │          │            │  Web       │
  │          │            │            │
  │          │◀──Result──│            │
  │          │            │            │
  │          │──────Save──────────────▶│
  │          │            │            │
  │◀─200────│            │            │
  │{id,txt}  │            │            │
  │          │            │            │
```

---

**Cette architecture est conçue pour être :**
- ✅ Simple à comprendre
- ✅ Facile à déployer
- ✅ Extensible pour le futur
- ✅ Sécurisée par défaut

