"""
Configuration de l'administration pour les utilisateurs.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Administration personnalisée pour le modèle User."""
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
