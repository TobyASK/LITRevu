"""
Configuration de l'administration pour les billets, critiques et abonnements.
"""
from django.contrib import admin
from .models import Ticket, Review, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Administration pour le modèle Ticket."""
    list_display = ('title', 'user', 'time_created')
    list_filter = ('time_created', 'user')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'time_created'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Administration pour le modèle Review."""
    list_display = ('headline', 'ticket', 'user', 'rating', 'time_created')
    list_filter = ('rating', 'time_created', 'user')
    search_fields = ('headline', 'body', 'user__username', 'ticket__title')
    date_hierarchy = 'time_created'


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """Administration pour le modèle UserFollows."""
    list_display = ('user', 'followed_user')
    list_filter = ('user', 'followed_user')
    search_fields = ('user__username', 'followed_user__username')
