from litrevu.settings import *  # noqa
import os

# Paramètres spécifiques au développement
DEBUG = True
ALLOWED_HOSTS = []

# Clé secrète de développement (jamais en prod)
key_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'key.txt'
)
try:
    with open(key_path, 'r', encoding='utf-8') as f:
        SECRET_KEY = f.read().strip()
except Exception:
    raise RuntimeError(
        "Le fichier 'key.txt' n'existe pas ou n'est pas lisible. "
        "Veuillez y placer votre clé secrète Django."
    )
if not SECRET_KEY:
    raise RuntimeError(
        (
            "Le fichier 'key.txt' est vide. "
            "Veuillez y placer votre clé secrète Django."
        )
    )
