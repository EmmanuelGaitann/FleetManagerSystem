from django.urls import path
from . import views

urlpatterns = [
    # Vue pour ajouter un nouvel utilisateur (accessible uniquement par les gestionnaires/superusers)
    path('creer/', views.UserCreateView.as_view(), name='user_create'),
    path('chauffeurs/creer/', views.ChauffeurCreateView.as_view(), name='chauffeur_create'),

]