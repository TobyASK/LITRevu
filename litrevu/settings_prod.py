
import os

# Paramètres spécifiques à la production
DEBUG = False
ALLOWED_HOSTS = ['your-production-domain.com']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError(
        ("La variable d'environnement DJANGO_SECRET_KEY doit être "
         "définie en production.")
    )
    if not SECRET_KEY:
        raise RuntimeError(
            "Le fichier 'key.txt' est vide. "
            "Veuillez y placer votre clé secrète Django."
        )

# Autres paramètres de sécurité recommandés
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
