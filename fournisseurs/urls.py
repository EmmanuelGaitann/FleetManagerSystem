# fournisseurs/urls.py (Contenu complet avec les chemins Pièce ajoutés)

from django.urls import path
from . import views

urlpatterns = [
    # CRUD Fournisseurs (EXISTANTS)
    path('fournisseurs/', views.fournisseur_list, name='fournisseur_list'),
    path('fournisseurs/ajouter/', views.fournisseur_create, name='fournisseur_create'),
    path('fournisseurs/modifier/<int:pk>/', views.fournisseur_update, name='fournisseur_update'),
    path('fournisseurs/supprimer/<int:pk>/', views.fournisseur_delete, name='fournisseur_delete'),

    # CRUD Pièces (NOUVEAU)
    path('pieces/', views.piece_list, name='piece_list'),
    path('pieces/ajouter/', views.piece_create, name='piece_create'),
    path('pieces/modifier/<int:pk>/', views.piece_update, name='piece_update'),
    path('pieces/supprimer/<int:pk>/', views.piece_delete, name='piece_delete'),
]