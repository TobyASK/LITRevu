"""
Formulaires pour l'authentification des utilisateurs.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


User = get_user_model()


class LoginForm(AuthenticationForm):
    """Formulaire de connexion personnalisé."""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur",
            'autocomplete': 'username',
            'aria-label': "Nom d'utilisateur"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'autocomplete': 'current-password',
            'aria-label': 'Mot de passe'
        })
    )


class SignupForm(UserCreationForm):
    """Formulaire d'inscription personnalisé."""

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur",
            'autocomplete': 'username',
            'aria-label': "Nom d'utilisateur"
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email (optionnel)',
            'autocomplete': 'email',
            'aria-label': 'Adresse email'
        })
        self.fields['email'].required = False
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'autocomplete': 'new-password',
            'aria-label': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe',
            'autocomplete': 'new-password',
            'aria-label': 'Confirmation du mot de passe'
        })
