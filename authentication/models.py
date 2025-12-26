"""
Modèle utilisateur personnalisé pour l'application LITRevu.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé étendant AbstractUser.
    Permet d'ajouter des champs supplémentaires si nécessaire.
    """
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        verbose_name="Photo de profil"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username
