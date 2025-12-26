"""
Vues pour les billets, critiques et abonnements.
"""
from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q

from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, FollowUserForm


User = get_user_model()


@login_required
def feed(request):
    """
    Affiche le flux principal de l'utilisateur.
    Contient les billets et critiques des utilisateurs suivis,
    ses propres billets et critiques, et les critiques en réponse
    à ses billets.
    """
    user = request.user

    # Récupérer les utilisateurs suivis
    followed_users = UserFollows.objects.filter(
        user=user
    ).values_list('followed_user', flat=True)

    # Billets visibles :
    # - billets de l'utilisateur connecté
    # - billets des utilisateurs suivis
    tickets = Ticket.objects.filter(
        Q(user=user) | Q(user__in=followed_users)
    )

    # Critiques visibles :
    # - critiques de l'utilisateur connecté
    # - critiques des utilisateurs suivis
    # - critiques en réponse aux billets de l'utilisateur connecté
    reviews = Review.objects.filter(
        Q(user=user) |
        Q(user__in=followed_users) |
        Q(ticket__user=user)
    )

    # Combiner et trier par date de création (antéchronologique)
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    # Marquer chaque post avec son type et si l'utilisateur en est l'auteur
    for post in posts:
        post.content_type = 'REVIEW' if isinstance(post, Review) else 'TICKET'
        post.is_own = post.user == user
        if post.content_type == 'TICKET':
            # Vérifier si ce billet a déjà une critique
            post.has_review = Review.objects.filter(ticket=post).exists()

    return render(request, 'reviews/feed.html', {'posts': posts})


@login_required
def user_posts(request):
    """Affiche les billets et critiques de l'utilisateur connecté."""
    user = request.user

    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    for post in posts:
        post.content_type = 'REVIEW' if isinstance(post, Review) else 'TICKET'
        post.is_own = True

    return render(request, 'reviews/user_posts.html', {'posts': posts})


# ============== TICKETS ==============

@login_required
def create_ticket(request):
    """Créer un nouveau billet."""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Votre billet a été créé avec succès.')
            return redirect('feed')
    else:
        form = TicketForm()

    return render(request, 'reviews/create_ticket.html', {'form': form})


@login_required
def edit_ticket(request, ticket_id):
    """Modifier un billet existant."""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Vérifier que l'utilisateur est l'auteur du billet
    if ticket.user != request.user:
        messages.error(request, "Vous ne pouvez pas modifier ce billet.")
        return redirect('feed')

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre billet a été modifié.')
            return redirect('user_posts')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews/edit_ticket.html', {
        'form': form,
        'ticket': ticket
    })


@login_required
def delete_ticket(request, ticket_id):
    """Supprimer un billet."""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Vérifier que l'utilisateur est l'auteur du billet
    if ticket.user != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer ce billet.")
        return redirect('feed')

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Votre billet a été supprimé.')
        return redirect('user_posts')

    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})


# ============== REVIEWS ==============

@login_required
def create_review(request, ticket_id):
    """Créer une critique en réponse à un billet existant."""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Vérifier si une critique existe déjà pour ce billet par cet utilisateur
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.error(
            request,
            'Vous avez déjà publié une critique pour ce billet.'
        )
        return redirect('feed')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Votre critique a été publiée.')
            return redirect('feed')
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {
        'form': form,
        'ticket': ticket
    })


@login_required
def create_ticket_and_review(request):
    """Créer un billet et une critique en une seule étape."""
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            # Créer le billet
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Créer la critique
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            messages.success(
                request,
                'Votre critique a été publiée avec succès.'
            )
            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'reviews/create_ticket_and_review.html', {
        'ticket_form': ticket_form,
        'review_form': review_form
    })


@login_required
def edit_review(request, review_id):
    """Modifier une critique existante."""
    review = get_object_or_404(Review, id=review_id)

    # Vérifier que l'utilisateur est l'auteur de la critique
    if review.user != request.user:
        messages.error(request, "Vous ne pouvez pas modifier cette critique.")
        return redirect('feed')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre critique a été modifiée.')
            return redirect('user_posts')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review
    })


@login_required
def delete_review(request, review_id):
    """Supprimer une critique."""
    review = get_object_or_404(Review, id=review_id)

    # Vérifier que l'utilisateur est l'auteur de la critique
    if review.user != request.user:
        messages.error(
            request,
            "Vous ne pouvez pas supprimer cette critique."
        )
        return redirect('feed')

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Votre critique a été supprimée.')
        return redirect('user_posts')

    return render(request, 'reviews/delete_review.html', {'review': review})


# ============== FOLLOWS ==============

@login_required
def follows(request):
    """Gérer les abonnements."""
    user = request.user

    if request.method == 'POST':
        form = FollowUserForm(request.POST, current_user=user)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_to_follow = User.objects.get(username=username)
            UserFollows.objects.create(user=user, followed_user=user_to_follow)
            messages.success(
                request,
                f"Vous suivez maintenant {username}."
            )
            return redirect('follows')
    else:
        form = FollowUserForm(current_user=user)

    # Utilisateurs que je suis
    following = UserFollows.objects.filter(user=user)

    # Utilisateurs qui me suivent
    followers = UserFollows.objects.filter(followed_user=user)

    return render(request, 'reviews/follows.html', {
        'form': form,
        'following': following,
        'followers': followers
    })


@login_required
def unfollow_user(request, user_id):
    """Ne plus suivre un utilisateur."""
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = get_object_or_404(
        UserFollows,
        user=request.user,
        followed_user=user_to_unfollow
    )

    if request.method == 'POST':
        follow.delete()
        messages.success(
            request,
            f"Vous ne suivez plus {user_to_unfollow.username}."
        )
        return redirect('follows')

    return render(request, 'reviews/unfollow_confirm.html', {
        'user_to_unfollow': user_to_unfollow
    })
