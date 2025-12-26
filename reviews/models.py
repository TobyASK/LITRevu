"""
Modèles pour les billets, critiques et abonnements de l'application LITRevu.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """
    Modèle représentant un billet (demande de critique).
    Un utilisateur crée un billet pour demander une critique sur un livre
    ou article.
    """
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(
        max_length=2048,
        blank=True,
        verbose_name="Description"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    image = models.ImageField(
        upload_to='tickets/',
        null=True,
        blank=True,
        verbose_name="Image"
    )
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Billet"
        verbose_name_plural = "Billets"
        ordering = ['-time_created']

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Modèle représentant une critique en réponse à un billet.
    """
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note"
    )
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(
        max_length=8192,
        blank=True,
        verbose_name="Commentaire"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Critique"
        verbose_name_plural = "Critiques"
        ordering = ['-time_created']

    def __str__(self):
        return f"{self.headline} - {self.ticket.title}"


class UserFollows(models.Model):
    """
    Modèle représentant la relation de suivi entre utilisateurs.
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"
