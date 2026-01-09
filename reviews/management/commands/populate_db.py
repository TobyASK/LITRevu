
from django.core.management.base import BaseCommand
from populate_db import main as populate_main


class Command(BaseCommand):
    help = (
        "Remplit la base de données avec des données de test "
        "(utilisateurs, billets, critiques, abonnements)."
    )

    def handle(self, *args, **options):
        populate_main()
