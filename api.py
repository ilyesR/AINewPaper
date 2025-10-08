#!/usr/bin/env python3
"""
API FastAPI pour la veille technologique utilisant l'API OpenAI + outil Web Search.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from datetime import datetime
from pathlib import Path
from openai import OpenAI
import uuid

app = FastAPI(
    title="AI News Paper API",
    description="API de veille technologique automatisée avec OpenAI",
    version="1.0.0"
)

# Servir les fichiers statiques si le dossier existe
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
API_KEY = os.getenv("OPENAI_API_KEY")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
VERBOSITY = os.getenv("OPENAI_VERBOSITY", "medium")
REASONING_EFFORT = os.getenv("OPENAI_REASONING_EFFORT", "medium")


class ResearchRequest(BaseModel):
    """Modèle de requête pour lancer une recherche"""
    subject: str
    previous_responses: Optional[List[str]] = []
    model: Optional[str] = None
    verbosity: Optional[str] = None
    reasoning_effort: Optional[str] = None


class ResearchResponse(BaseModel):
    """Modèle de réponse pour une recherche"""
    research_id: str
    status: str
    message: str
    output_file: Optional[str] = None
    metadata_file: Optional[str] = None


def perform_research(
    subject: str,
    previous_responses: List[str],
    research_id: str,
    model: str = MODEL,
    verbosity: str = VERBOSITY,
    reasoning_effort: str = REASONING_EFFORT
) -> dict:
    """
    Effectue la recherche et sauvegarde les résultats.
    """
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY non définie dans les variables d'environnement")
    
    client = OpenAI(api_key=API_KEY)
    
    # Préparer le sujet JSON
    subject_json = {
        "Subject": subject,
        "PreviousResponses": previous_responses
    }
    
    developer_instruction = (
        "Tu es un assistant de veille technologique expert. Ta mission est de faire une recherche "
        "approfondie et structurée sur un sujet donné, en utilisant l'outil Web Search pour trouver "
        "des informations fiables, récentes et pertinentes.\n\n"
        "Fait des recherches sur les nouvelles avancées, les plus récentes possible.\n\n"
        "Le sujet sera fourni au format JSON dans le message utilisateur.\n"
        "Si la catégorie 'PreviousResponses' contient quelque chose, analyse les anciennes réponses "
        "et évite de répéter les mêmes informations."
    )
    
    # Messages pour le modèle
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
    
    # Appel à l'API
    response = client.responses.create(
        model=model,
        input=input_messages,
        text={
            "format": {"type": "text"},
            "verbosity": verbosity
        },
        reasoning={"effort": reasoning_effort},
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
    
    # Extraction du texte de sortie
    output_text = getattr(response, "output_text", None)
    if not output_text:
        fragments = []
        for item in getattr(response, "output", []):
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    fragments.append(c.get("text", ""))
        output_text = "\n\n".join(fragments) if fragments else "[Aucune sortie texte trouvée]"
    
    # Sauvegarde des résultats
    now = datetime.utcnow().isoformat() + "Z"
    
    output_file = OUTPUT_DIR / f"{research_id}_output.txt"
    metadata_file = OUTPUT_DIR / f"{research_id}_metadata.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- Résultat généré le {now} (UTC) ---\n\n")
        f.write(f"Sujet: {subject}\n\n")
        f.write("=" * 80 + "\n\n")
        f.write(output_text)
    
    metadata = {
        "research_id": research_id,
        "model": model,
        "subject": subject,
        "previous_responses": previous_responses,
        "created_at": now,
        "output_file": str(output_file),
        "output_raw": response.model_dump()
    }
    
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    return {
        "output_file": str(output_file),
        "metadata_file": str(metadata_file),
        "output_text": output_text,
        "created_at": now
    }


@app.get("/")
async def root():
    """Page d'accueil de l'API - Redirige vers l'interface web si disponible"""
    static_index = Path("static/index.html")
    if static_index.exists():
        return FileResponse(static_index)
    
    return {
        "message": "Bienvenue sur l'API AI News Paper",
        "version": "1.0.0",
        "endpoints": {
            "POST /research": "Lancer une nouvelle recherche",
            "GET /health": "Vérifier l'état de l'API",
            "GET /results/{research_id}": "Récupérer les résultats d'une recherche",
            "GET /latest": "Récupérer la dernière recherche",
            "GET /list": "Lister toutes les recherches"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
async def health_check():
    """Vérifier l'état de l'API"""
    api_key_configured = API_KEY is not None and len(API_KEY) > 0
    return {
        "status": "healthy" if api_key_configured else "degraded",
        "api_key_configured": api_key_configured,
        "model": MODEL,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/research", response_model=ResearchResponse)
async def create_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    Lancer une nouvelle recherche de veille technologique.
    
    La recherche est effectuée en arrière-plan pour ne pas bloquer la réponse.
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY non configurée. Veuillez définir la variable d'environnement."
        )
    
    # Générer un ID unique pour cette recherche
    research_id = str(uuid.uuid4())
    
    # Utiliser les paramètres par défaut ou ceux fournis
    model = request.model or MODEL
    verbosity = request.verbosity or VERBOSITY
    reasoning_effort = request.reasoning_effort or REASONING_EFFORT
    
    try:
        # Effectuer la recherche de manière synchrone (pour l'instant)
        result = perform_research(
            subject=request.subject,
            previous_responses=request.previous_responses,
            research_id=research_id,
            model=model,
            verbosity=verbosity,
            reasoning_effort=reasoning_effort
        )
        
        return ResearchResponse(
            research_id=research_id,
            status="completed",
            message="Recherche terminée avec succès",
            output_file=result["output_file"],
            metadata_file=result["metadata_file"]
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la recherche: {str(e)}"
        )


@app.get("/results/{research_id}")
async def get_results(research_id: str, format: str = "json"):
    """
    Récupérer les résultats d'une recherche par son ID.
    
    - **format**: 'json' pour les métadonnées complètes, 'text' pour le texte brut
    """
    output_file = OUTPUT_DIR / f"{research_id}_output.txt"
    metadata_file = OUTPUT_DIR / f"{research_id}_metadata.json"
    
    if not metadata_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Recherche {research_id} non trouvée"
        )
    
    if format == "text":
        if not output_file.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Fichier de sortie pour {research_id} non trouvé"
            )
        return FileResponse(
            path=output_file,
            media_type="text/plain",
            filename=f"research_{research_id}.txt"
        )
    
    # Format JSON par défaut
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    # Ajouter le texte de sortie si disponible
    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            metadata["output_text"] = f.read()
    
    return metadata


@app.get("/latest")
async def get_latest():
    """Récupérer la dernière recherche effectuée"""
    metadata_files = list(OUTPUT_DIR.glob("*_metadata.json"))
    
    if not metadata_files:
        raise HTTPException(
            status_code=404,
            detail="Aucune recherche trouvée"
        )
    
    # Trier par date de modification
    latest_file = max(metadata_files, key=lambda p: p.stat().st_mtime)
    
    with open(latest_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    # Ajouter le texte de sortie
    research_id = metadata.get("research_id")
    output_file = OUTPUT_DIR / f"{research_id}_output.txt"
    
    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            metadata["output_text"] = f.read()
    
    return metadata


@app.get("/list")
async def list_researches():
    """Lister toutes les recherches disponibles"""
    metadata_files = list(OUTPUT_DIR.glob("*_metadata.json"))
    
    researches = []
    for metadata_file in sorted(metadata_files, key=lambda p: p.stat().st_mtime, reverse=True):
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            researches.append({
                "research_id": metadata.get("research_id"),
                "subject": metadata.get("subject"),
                "created_at": metadata.get("created_at"),
                "model": metadata.get("model")
            })
    
    return {
        "total": len(researches),
        "researches": researches
    }


@app.delete("/results/{research_id}")
async def delete_research(research_id: str):
    """Supprimer une recherche et ses fichiers associés"""
    output_file = OUTPUT_DIR / f"{research_id}_output.txt"
    metadata_file = OUTPUT_DIR / f"{research_id}_metadata.json"
    
    if not metadata_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Recherche {research_id} non trouvée"
        )
    
    # Supprimer les fichiers
    if output_file.exists():
        output_file.unlink()
    if metadata_file.exists():
        metadata_file.unlink()
    
    return {
        "message": f"Recherche {research_id} supprimée avec succès"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

