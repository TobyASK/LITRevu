@echo off
REM === Script de démarrage LITRevu (Backend - LOCAL) ===
cd /d %~dp0

REM Activer l'environnement virtuel s'il existe
IF EXIST "venv\Scripts\activate.bat" (
	call venv\Scripts\activate.bat
	echo Environnement virtuel activé.
) ELSE (
	echo Aucun environnement virtuel trouvé. Créez-en un avec : python -m venv venv
	echo Le script continue sans venv.
)

REM Installer les dépendances
echo Installation des dépendances...
pip install -r requirements.txt

REM Appliquer les migrations
echo Application des migrations...
set DJANGO_ENV=local
python manage.py migrate

REM Peupler la base de données de test (optionnel, sans risque)
echo Remplissage des données de test...
set DJANGO_ENV=local
python manage.py populate_db

REM Lancer le serveur Django
echo Démarrage du serveur de développement Django sur le port 8001...
set DJANGO_ENV=local
python manage.py runserver 8001

REM Pour démarrer le frontend, ajoutez la commande correspondante ci-dessous
REM Exemple pour React : cd frontend && npm start
