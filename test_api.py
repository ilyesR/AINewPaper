#!/usr/bin/env python3
"""
Script de test pour l'API AI News Paper
"""

import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000"  # Changez pour votre URL Railway si déployé

def test_health():
    """Test de l'endpoint /health"""
    print("🔍 Test de /health...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Réponse: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_create_research():
    """Test de création d'une recherche"""
    print("📝 Test de /research...")
    
    payload = {
        "subject": "Les dernières avancées en intelligence artificielle générative en octobre 2025",
        "previous_responses": [
            "Rapport sur les modèles de langage de 2024"
        ]
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{API_URL}/research", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Réponse: {json.dumps(data, indent=2)}\n")
        return data.get("research_id")
    else:
        print(f"Erreur: {response.text}\n")
        return None

def test_get_results(research_id):
    """Test de récupération des résultats"""
    if not research_id:
        print("⚠️  Pas de research_id, skip du test\n")
        return
    
    print(f"📊 Test de /results/{research_id}...")
    response = requests.get(f"{API_URL}/results/{research_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Sujet: {data.get('subject')}")
        print(f"Créé le: {data.get('created_at')}")
        print(f"Modèle: {data.get('model')}")
        print(f"Longueur du texte: {len(data.get('output_text', ''))} caractères\n")
    else:
        print(f"Erreur: {response.text}\n")

def test_list_researches():
    """Test de listing des recherches"""
    print("📋 Test de /list...")
    response = requests.get(f"{API_URL}/list")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total: {data.get('total')} recherches")
        for research in data.get('researches', [])[:3]:  # Afficher les 3 premières
            print(f"  - {research.get('subject')} ({research.get('created_at')})")
        print()
    else:
        print(f"Erreur: {response.text}\n")

def test_latest():
    """Test de récupération de la dernière recherche"""
    print("🕒 Test de /latest...")
    response = requests.get(f"{API_URL}/latest")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Sujet: {data.get('subject')}")
        print(f"Créé le: {data.get('created_at')}\n")
    else:
        print(f"Erreur: {response.text}\n")

def main():
    """Exécuter tous les tests"""
    print("=" * 80)
    print("Tests de l'API AI News Paper")
    print("=" * 80 + "\n")
    
    try:
        # Test 1: Health check
        if not test_health():
            print("❌ L'API n'est pas accessible ou la configuration est incorrecte")
            return
        
        # Test 2: Lister les recherches existantes
        test_list_researches()
        
        # Test 3: Récupérer la dernière recherche
        test_latest()
        
        # Test 4: Créer une nouvelle recherche (peut être long)
        print("⚠️  La création d'une recherche peut prendre plusieurs minutes...")
        choice = input("Voulez-vous lancer une nouvelle recherche ? (o/n): ")
        
        if choice.lower() == 'o':
            research_id = test_create_research()
            
            # Test 5: Récupérer les résultats
            if research_id:
                test_get_results(research_id)
        
        print("✅ Tests terminés !")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Impossible de se connecter à {API_URL}")
        print("Vérifiez que l'API est bien lancée avec: uvicorn api:app --reload")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()

