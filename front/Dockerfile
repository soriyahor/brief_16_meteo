# Utilisez une image de Python officielle en tant qu'image de base
FROM python:3.11-alpine

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le contenu du dossier "template" dans le répertoire de travail du conteneur
COPY . .

# Exposez le port sur lequel votre serveur HTTP Python fonctionnera
EXPOSE 8001

# Commande pour démarrer votre serveur HTTP Python
CMD ["python", "-m", "http.server", "8001"]
