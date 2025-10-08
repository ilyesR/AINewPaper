# Dockerfile pour l'API AI News Paper
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer le dossier outputs
RUN mkdir -p outputs

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

