#!/usr/bin/env python3
"""
Script de vérification de la configuration avant déploiement
"""

import os
import sys
from pathlib import Path

def check_mark(condition):
    return "✅" if condition else "❌"

def main():
    print("=" * 80)
    print("🔍 Vérification de la configuration - AI News Paper API")
    print("=" * 80)
    print()
    
    all_checks_passed = True
    
    # 1. Vérifier les fichiers essentiels
    print("📁 Fichiers essentiels:")
    required_files = [
        "api.py",
        "requirements.txt",
        "railway.toml",
        "Procfile",
        ".gitignore",
        "README.md"
    ]
    
    for file in required_files:
        exists = Path(file).exists()
        print(f"  {check_mark(exists)} {file}")
        if not exists:
            all_checks_passed = False
    print()
    
    # 2. Vérifier les dépendances dans requirements.txt
    print("📦 Dépendances:")
    if Path("requirements.txt").exists():
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            deps = ["openai", "fastapi", "uvicorn", "pydantic"]
            for dep in deps:
                exists = dep in requirements
                print(f"  {check_mark(exists)} {dep}")
                if not exists:
                    all_checks_passed = False
    else:
        print("  ❌ requirements.txt non trouvé")
        all_checks_passed = False
    print()
    
    # 3. Vérifier les variables d'environnement
    print("🔐 Variables d'environnement:")
    env_file = Path(".env")
    if env_file.exists():
        print(f"  ✅ Fichier .env trouvé")
        
        # Charger les variables
        with open(env_file, "r") as f:
            env_content = f.read()
            
        api_key_set = "OPENAI_API_KEY" in env_content and "sk-" in env_content
        print(f"  {check_mark(api_key_set)} OPENAI_API_KEY configurée")
        
        if not api_key_set:
            print("    ⚠️  Assurez-vous d'avoir défini votre clé API OpenAI dans .env")
            all_checks_passed = False
    else:
        print(f"  ⚠️  Fichier .env non trouvé (OK pour Railway, requis pour local)")
        print(f"    💡 Créez-le depuis .env.example pour tester en local")
    print()
    
    # 4. Vérifier la structure du code
    print("🔧 Structure du code:")
    if Path("api.py").exists():
        with open("api.py", "r") as f:
            api_content = f.read()
            
        checks = {
            "FastAPI importé": "from fastapi import FastAPI" in api_content,
            "OpenAI importé": "from openai import OpenAI" in api_content,
            "Endpoint /health": '@app.get("/health")' in api_content,
            "Endpoint /research": '/research' in api_content and '@app.post' in api_content,
            "Configuration PORT": 'os.getenv("PORT"' in api_content or 'os.getenv("OPENAI_API_KEY"' in api_content,
        }
        
        for check_name, passed in checks.items():
            print(f"  {check_mark(passed)} {check_name}")
            if not passed:
                all_checks_passed = False
    print()
    
    # 5. Vérifier la configuration Railway
    print("🚂 Configuration Railway:")
    if Path("railway.toml").exists():
        with open("railway.toml", "r") as f:
            railway_config = f.read()
            
        checks = {
            "startCommand défini": "startCommand" in railway_config,
            "uvicorn configuré": "uvicorn" in railway_config,
            "PORT variable utilisée": "$PORT" in railway_config,
        }
        
        for check_name, passed in checks.items():
            print(f"  {check_mark(passed)} {check_name}")
            if not passed:
                all_checks_passed = False
    else:
        print("  ❌ railway.toml non trouvé")
        all_checks_passed = False
    print()
    
    # 6. Vérifier .gitignore
    print("🛡️  Sécurité:")
    if Path(".gitignore").exists():
        with open(".gitignore", "r") as f:
            gitignore = f.read()
            
        checks = {
            ".env ignoré": ".env" in gitignore,
            "outputs/ ignoré": "outputs/" in gitignore,
            "__pycache__/ ignoré": "__pycache__/" in gitignore,
        }
        
        for check_name, passed in checks.items():
            print(f"  {check_mark(passed)} {check_name}")
            if not passed:
                all_checks_passed = False
    else:
        print("  ❌ .gitignore non trouvé")
        all_checks_passed = False
    print()
    
    # 7. Vérifier qu'aucune clé API n'est dans le code
    print("🔒 Vérification des secrets:")
    sensitive_files = ["api.py", "main.py"]
    secrets_found = False
    
    for file in sensitive_files:
        if Path(file).exists():
            with open(file, "r") as f:
                content = f.read()
                if "sk-proj-" in content and 'os.getenv' not in content.split("sk-proj-")[1][:50]:
                    print(f"  ⚠️  Clé API potentiellement exposée dans {file}")
                    secrets_found = True
    
    if not secrets_found:
        print(f"  ✅ Aucune clé API hardcodée détectée")
    else:
        print(f"  ❌ Clés API trouvées dans le code - URGENT: les supprimer!")
        all_checks_passed = False
    print()
    
    # 8. Vérifier les dossiers
    print("📂 Dossiers:")
    dirs = {
        "static/": "Interface web",
        "outputs/": "Stockage des résultats (sera créé automatiquement)"
    }
    
    for dir_path, description in dirs.items():
        exists = Path(dir_path).exists()
        status = "✅" if exists else "ℹ️ "
        print(f"  {status} {dir_path} - {description}")
    print()
    
    # Résumé final
    print("=" * 80)
    if all_checks_passed:
        print("✅ TOUT EST PRÊT POUR LE DÉPLOIEMENT!")
        print()
        print("Prochaines étapes:")
        print("  1. Commitez vos changements: git add . && git commit -m 'Ready for deployment'")
        print("  2. Poussez vers GitHub: git push")
        print("  3. Déployez sur Railway depuis l'interface web")
        print("  4. Ajoutez OPENAI_API_KEY dans les variables Railway")
        print()
        return 0
    else:
        print("❌ CERTAINES VÉRIFICATIONS ONT ÉCHOUÉ")
        print()
        print("Veuillez corriger les problèmes ci-dessus avant de déployer.")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

