# maintenance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # CRUD Entretien (Avec Formset)
    path('entretiens/', views.entretien_list, name='entretien_list'),
    path('entretiens/ajouter/', views.entretien_create, name='entretien_create'),
    path('entretiens/modifier/<int:pk>/', views.entretien_update, name='entretien_update'),
    path('entretiens/supprimer/<int:pk>/', views.entretien_delete, name='entretien_delete'),
]