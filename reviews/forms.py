"""
Formulaires pour les billets, critiques et abonnements.
"""
from django import forms
from django.contrib.auth import get_user_model

from .models import Ticket, Review, UserFollows


User = get_user_model()


class TicketForm(forms.ModelForm):
    """Formulaire pour créer/modifier un billet."""

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du livre ou article',
                'aria-label': 'Titre du livre ou article'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description (optionnel)',
                'rows': 5,
                'aria-label': 'Description'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'aria-label': 'Image de couverture'
            })
        }


class ReviewForm(forms.ModelForm):
    """Formulaire pour créer/modifier une critique."""

    RATING_CHOICES = [(i, str(i)) for i in range(6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'rating-radio',
            'aria-label': 'Note de 0 à 5'
        }),
        label='Note'
    )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la critique',
                'aria-label': 'Titre de la critique'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Votre critique (optionnel)',
                'rows': 5,
                'aria-label': 'Contenu de la critique'
            })
        }


class FollowUserForm(forms.Form):
    """Formulaire pour suivre un utilisateur."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur à suivre",
            'aria-label': "Nom d'utilisateur à suivre"
        }),
        label="Nom d'utilisateur"
    )

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Vérifier que l'utilisateur existe
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(
                f"L'utilisateur '{username}' n'existe pas."
            )

        # Vérifier qu'on ne se suit pas soi-même
        if self.current_user and user_to_follow == self.current_user:
            raise forms.ValidationError(
                "Vous ne pouvez pas vous suivre vous-même."
            )

        # Vérifier qu'on ne suit pas déjà cet utilisateur
        if self.current_user and UserFollows.objects.filter(
            user=self.current_user,
            followed_user=user_to_follow
        ).exists():
            raise forms.ValidationError(
                f"Vous suivez déjà '{username}'."
            )

        return username
