"""
URLs pour l'application authentication.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
