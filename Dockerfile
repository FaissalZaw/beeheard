# Image de base légère, version fixée pour la reproductibilité
FROM python:3.13-slim

# Empêche Python d'écrire des fichiers .pyc et force l'affichage immédiat des logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Les dépendances sont installées avant la copie du code, afin de tirer
# parti du cache de construction lorsque seul le code change
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Création du répertoire de persistance
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["sh", "-c", "python3 scripts/initialiser_donnees.py && python3 scripts/donnees_demonstration.py && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
