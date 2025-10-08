#!/usr/bin/env python3
"""
veille_research.py
Script de veille technologique utilisant l'API OpenAI + outil Web Search.
"""

import json
import sys
import os
from datetime import datetime
from openai import OpenAI

# Clé API depuis les variables d'environnement
API_KEY = os.getenv("OPENAI_API_KEY")

# Fichiers utilisés
INPUT_FILE = "subject.json"
OUTPUT_TEXT_FILE = "output.txt"
METADATA_FILE = "metadata.json"

# Paramètres du modèle
MODEL = "gpt-5"
VERBOSITY = "medium"
REASONING_EFFORT = "medium"

def load_subject(path):
    """Charge le sujet JSON à traiter."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERREUR] Impossible de lire '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Vérifier que la clé API est définie
    if not API_KEY:
        print("[ERREUR] La variable d'environnement OPENAI_API_KEY n'est pas définie.", file=sys.stderr)
        print("Veuillez définir votre clé API OpenAI dans les variables d'environnement.", file=sys.stderr)
        sys.exit(1)
    
    client = OpenAI(api_key=API_KEY)

    subject_json = load_subject(INPUT_FILE)

    developer_instruction = (
        "Tu es un assistant de veille technologique expert. Ta mission est de faire une recherche "
        "approfondie et structurée sur un sujet donné, en utilisant l'outil Web Search pour trouver "
        "des informations fiables, récentes et pertinentes.\n\n"
        "Fait des recherches sur les nouvelles avancées, les plus récentes possible.\n\n"
        "Le sujet sera fourni au format JSON dans le message utilisateur.\n"
        "Si la catégorie 'PreviousResponses' contient quelque chose, analyse les anciennes réponses "
        "et évite de répéter les mêmes informations."
    )

    # Messages envoyés au modèle
    input_messages = [
        {
            "role": "developer",
            "content": [
                {"type": "input_text", "text": developer_instruction}
            ]
        },
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": json.dumps(subject_json, ensure_ascii=False, indent=2)}
            ]
        }
    ]

    print("[INFO] Envoi de la requête à l'API...")
    try:
        response = client.responses.create(
            model=MODEL,
            input=input_messages,
            text={
                "format": {"type": "text"},
                "verbosity": VERBOSITY
            },
            reasoning={"effort": REASONING_EFFORT},
            tools=[
                {
                    "type": "web_search",
                    "user_location": {"type": "approximate"},
                    "search_context_size": "high"
                }
            ],
            store=True,
            include=[
                "reasoning.encrypted_content",
                "web_search_call.action.sources"
            ]
        )
    except Exception as e:
        print(f"[ERREUR] Échec de l'appel API : {e}", file=sys.stderr)
        sys.exit(1)

    # Extraction du texte de sortie
    output_text = getattr(response, "output_text", None)
    if not output_text:
        fragments = []
        for item in getattr(response, "output", []):
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    fragments.append(c.get("text", ""))
        output_text = "\n\n".join(fragments) if fragments else "[Aucune sortie texte trouvée]"

    # Sauvegarde dans un fichier texte
    now = datetime.utcnow().isoformat() + "Z"
    with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as f:
        f.write(f"--- Résultat généré le {now} (UTC) ---\n\n")
        f.write(output_text)

    # Sauvegarde des métadonnées
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "model": MODEL,
                "created_at": now,
                "input_file": INPUT_FILE,
                "output_raw": response.model_dump()  # dump brut de l'objet réponse
            },
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"[OK] Résultat écrit dans '{OUTPUT_TEXT_FILE}'")
    print(f"[OK] Métadonnées écrites dans '{METADATA_FILE}'")

if __name__ == "__main__":
    main()
