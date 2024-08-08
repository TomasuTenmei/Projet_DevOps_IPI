# Utilise l'image officielle de Python
FROM python:3.11-slim

# Configure le répertoire de travail
WORKDIR /app

# Copie le fichier de dépendances
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste des fichiers de l'application
COPY . .

# Expose le port de l'application
EXPOSE 80

# Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
