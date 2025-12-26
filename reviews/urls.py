"""
URLs pour l'application reviews.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Flux principal
    path('feed/', views.feed, name='feed'),
    path('posts/', views.user_posts, name='user_posts'),

    # Tickets
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path(
        'ticket/<int:ticket_id>/edit/',
        views.edit_ticket,
        name='edit_ticket'
    ),
    path(
        'ticket/<int:ticket_id>/delete/',
        views.delete_ticket,
        name='delete_ticket'
    ),

    # Reviews
    path(
        'ticket/<int:ticket_id>/review/',
        views.create_review,
        name='create_review'
    ),
    path(
        'review/create/',
        views.create_ticket_and_review,
        name='create_ticket_and_review'
    ),
    path(
        'review/<int:review_id>/edit/',
        views.edit_review,
        name='edit_review'
    ),
    path(
        'review/<int:review_id>/delete/',
        views.delete_review,
        name='delete_review'
    ),

    # Follows
    path('follows/', views.follows, name='follows'),
    path(
        'unfollow/<int:user_id>/',
        views.unfollow_user,
        name='unfollow_user'
    ),
]
