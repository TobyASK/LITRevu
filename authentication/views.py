"""
Vues pour l'authentification des utilisateurs.
"""
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import LoginForm, SignupForm


class CustomLoginView(LoginView):
    """Vue de connexion personnalisée."""

    form_class = LoginForm
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('feed')


class SignupView(CreateView):
    """Vue d'inscription personnalisée."""

    form_class = SignupForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        """Connecter l'utilisateur après inscription."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def logout_view(request):
    """Vue de déconnexion."""
    logout(request)
    return redirect('login')
