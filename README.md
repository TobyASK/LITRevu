# LITRevu

Application web Django permettant de demander, publier et consulter des critiques de livres et d'articles.

## 📖 Description

LITRevu est une plateforme communautaire où les utilisateurs peuvent :
- **Demander des critiques** en créant des billets pour des livres ou articles
- **Publier des critiques** en réponse aux billets d'autres utilisateurs
- **Suivre d'autres utilisateurs** pour voir leurs billets et critiques dans leur flux
- **Gérer leurs publications** (modifier, supprimer leurs propres billets et critiques)

## 🚀 Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Démarrage rapide (Windows)

Un script automatisé est fourni pour configurer et lancer le projet en une seule commande :

1. **Cloner le repository**
   ```bash
   git clone <url-du-repository>
   cd <nom-du-repository>
   ```

2. **Lancer le script de démarrage**
   
   Dans l'invite de commandes :
   ```cmd
   .\start_backend.bat
   ```

Ce script :
- Active l'environnement virtuel (ou invite à le créer)
- Installe les dépendances
- Applique les migrations
- Remplit la base de données de test
- Lance le serveur Django sur le port 8001

3. **Accéder à l'application**

Ouvrez votre navigateur à l'adresse : http://127.0.0.1:8001

---

### Installation manuelle (tous systèmes)

Si vous ne souhaitez pas utiliser le script, suivez ces étapes :

1. Créez et activez un environnement virtuel
2. Installez les dépendances : `pip install -r requirements.txt`
3. Appliquez les migrations : `python manage.py migrate`
4. (Optionnel) Remplissez la base de test : `python populate_db.py`
5. Lancez le serveur : `python manage.py runserver 8001`
6. Accédez à l'application sur http://127.0.0.1:8001

## 👥 Comptes de test

L'application inclut des données de test avec les comptes suivants :

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| admin | admin123 | Administrateur |
| alice | alice123 | Utilisateur |
| bob | bob123 | Utilisateur |
| charlie | charlie123 | Utilisateur |
| diane | diane123 | Utilisateur |

### Relations de suivi pré-configurées :
- Alice suit Bob et Charlie
- Bob suit Alice et Diane
- Charlie suit Alice et Bob
- Diane suit Alice

## 🏗️ Structure du projet

```
Django9/
├── authentication/          # Application d'authentification
│   ├── models.py           # Modèle User personnalisé
│   ├── views.py            # Vues de connexion/inscription
│   ├── forms.py            # Formulaires d'authentification
│   └── urls.py             # URLs d'authentification
├── reviews/                 # Application principale
│   ├── models.py           # Modèles Ticket, Review, UserFollows
│   ├── views.py            # Vues CRUD et flux
│   ├── forms.py            # Formulaires
│   └── urls.py             # URLs de l'application
├── templates/               # Gabarits HTML (frontend généré côté serveur par Django)
│   ├── base.html           # Template de base
│   ├── authentication/     # Templates auth
│   └── reviews/            # Templates reviews
├── litrevu/                 # Configuration Django
│   ├── settings.py
│   └── urls.py
├── static/                  # Fichiers statiques (CSS, images)
├── media/                   # Fichiers uploadés
├── db.sqlite3              # Base de données SQLite
├── manage.py
├── populate_db.py          # Script de données de test
├── requirements.txt        # Dépendances Python
├── start_backend.bat       # Script de démarrage automatisé (Windows)
└── README.md
```

## ✨ Fonctionnalités

### Authentification
- ✅ Inscription avec nom d'utilisateur et mot de passe
- ✅ Connexion / Déconnexion
- ✅ Protection des pages pour utilisateurs connectés uniquement

### Billets (Tickets)
- ✅ Créer un billet pour demander une critique
- ✅ Modifier ses propres billets
- ✅ Supprimer ses propres billets
- ✅ Ajouter une image de couverture

### Critiques (Reviews)
- ✅ Créer une critique en réponse à un billet
- ✅ Créer un billet et une critique en même temps
- ✅ Modifier ses propres critiques
- ✅ Supprimer ses propres critiques
- ✅ Système de notation de 0 à 5

### Flux
- ✅ Affichage des billets et critiques des utilisateurs suivis
- ✅ Affichage de ses propres billets et critiques
- ✅ Affichage des critiques en réponse à ses billets
- ✅ Tri antéchronologique (plus récents en premier)

### Abonnements
- ✅ Suivre un utilisateur par son nom
- ✅ Ne plus suivre un utilisateur
- ✅ Voir la liste de ses abonnements
- ✅ Voir la liste de ses abonnés

## ♿ Accessibilité

L'application respecte les bonnes pratiques WCAG :
- Labels explicites pour tous les champs de formulaire
- Attributs aria-label pour les éléments interactifs
- Contraste suffisant entre texte et fond
- Navigation au clavier possible
- Skip link pour accéder au contenu principal
- Support des préférences de mouvement réduit

## 🛠️ Technologies utilisées

- **Framework** : Django 5.2
- **Base de données** : SQLite
- **Frontend** : HTML5, CSS3 (via templates Django, pas d'app frontend séparée)
- **Langage** : Python 3.12

## 📝 Administration

Accédez à l'interface d'administration Django :
- URL : http://127.0.0.1:8000/admin/
- Utilisateur : admin
- Mot de passe : admin123

## 📜 Conformité PEP8

Le code respecte les conventions PEP8. Pour vérifier :

```bash
pip install flake8
flake8 --max-line-length=88 authentication reviews litrevu
```

## 📄 Licence

Projet réalisé dans le cadre d'une formation OpenClassrooms.
