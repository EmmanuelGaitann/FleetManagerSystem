# utilisateurs/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Vue pour ajouter un nouvel utilisateur (accessible uniquement par les gestionnaires/superusers)
    path('creer/', views.UserCreateView.as_view(), name='user_create'),
    # Ajoutez ici d'autres chemins de gestion d'utilisateurs (liste, modification...)
]