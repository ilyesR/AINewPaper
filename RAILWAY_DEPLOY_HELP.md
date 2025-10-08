# 🚂 Aide au déploiement Railway

## Votre repository GitHub

```
Repository: https://github.com/ilyesR/AINewPaper
Branch: main
Status: ✅ Tout est synchronisé
```

## Méthode Alternative : Railway CLI

Si votre repo n'apparaît pas dans l'interface web, utilisez le CLI :

### Installation

```bash
# Installer Railway CLI
npm install -g @railway/cli
```

### Déploiement

```bash
# 1. Se connecter à Railway
railway login

# 2. Initialiser le projet
railway init

# 3. Lier le repo GitHub
railway link

# 4. Déployer
railway up

# 5. Ajouter la variable d'environnement
railway variables set OPENAI_API_KEY=VOTRE_CLE_API_ICI

# 6. Générer un domaine
railway domain
```

## Vérifications importantes

### 1. GitHub App Installation

Vérifiez que Railway a accès à votre compte GitHub :

👉 https://github.com/settings/installations

Assurez-vous que **Railway** est installé et a accès à **AINewPaper**.

### 2. Repository Settings

Dans votre repo GitHub, vérifiez :
- ✅ Le repo n'est pas archivé
- ✅ Vous êtes owner ou admin
- ✅ Le repo contient bien les fichiers (railway.toml, etc.)

### 3. Railway Account

Sur Railway :
- ✅ Votre compte GitHub est connecté
- ✅ Vous avez confirmé votre email
- ✅ Vous êtes sur le bon compte (si vous en avez plusieurs)

## Déploiement manuel via l'interface

### Étape par étape

1. **Connectez-vous sur** https://railway.app/

2. **Cliquez sur "New Project"**

3. **Sélectionnez "Deploy from GitHub repo"**

4. **Si le repo n'apparaît pas** :
   - Cliquez sur le lien "Configure GitHub App" en bas
   - Ou cherchez le repo par son nom : "AINewPaper"
   - Ou rafraîchissez la page

5. **Sélectionnez** : `ilyesR/AINewPaper`

6. **Railway détectera** automatiquement `railway.toml`

7. **Ajoutez la variable d'environnement** :
   - Allez dans l'onglet "Variables"
   - Cliquez sur "+ New Variable"
   - Nom : `OPENAI_API_KEY`
   - Valeur : Votre clé OpenAI (sk-proj-...)

8. **Générez un domaine** :
   - Allez dans l'onglet "Settings"
   - Section "Networking"
   - Cliquez sur "Generate Domain"

## Problèmes courants

### "Repository not found"

**Solution** : Donnez les permissions à Railway
1. GitHub → Settings → Installations
2. Railway → Configure
3. Repository access → All repositories (ou sélectionnez AINewPaper)

### "Build failed"

**Causes possibles** :
- Variable OPENAI_API_KEY manquante
- Fichier railway.toml mal configuré

**Solution** :
Vérifiez les logs du build dans Railway

### "Application error"

**Causes** :
- Port non configuré
- Clé API invalide

**Solution** :
1. Vérifiez que PORT est en variable d'environnement (Railway l'ajoute automatiquement)
2. Vérifiez votre clé OPENAI_API_KEY

## Support

Si rien ne fonctionne :

1. **Railway Discord** : https://discord.gg/railway
2. **Railway Docs** : https://docs.railway.app/
3. **GitHub Issues Railway** : https://github.com/railwayapp/railway/issues

## Configuration actuelle de votre projet

Fichiers présents :
- ✅ railway.toml
- ✅ Procfile
- ✅ requirements.txt
- ✅ runtime.txt
- ✅ api.py
- ✅ Tous les fichiers nécessaires

Tout est prêt pour le déploiement ! 🚀

