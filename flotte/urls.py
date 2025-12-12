# flotte/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --------------------------------------------------
    # 1. Dashboard et Alertes
    # --------------------------------------------------
    # La racine de l'application 'flotte' dirige vers le tableau de bord des alertes
    path('', views.alerte_list, name='alerte_list'),
    path('dashboard/', views.dashboard_view, name='dashboard'), # Reste pour une vue plus générale

    # --------------------------------------------------
    # 2. CRUD Départements
    # --------------------------------------------------
    path('departements/', views.departement_list, name='departement_list'),
    path('departements/ajouter/', views.departement_create, name='departement_create'),
    path('departements/modifier/<int:pk>/', views.departement_update, name='departement_update'),
    path('departements/supprimer/<int:pk>/', views.departement_delete, name='departement_delete'),

    # --------------------------------------------------
    # 3. CRUD Véhicules
    # --------------------------------------------------
    path('vehicules/', views.vehicule_list, name='vehicule_list'),
    path('vehicules/ajouter/', views.vehicule_create, name='vehicule_create'),
    path('vehicules/modifier/<int:pk>/', views.vehicule_update, name='vehicule_update'),
    path('vehicules/supprimer/<int:pk>/', views.vehicule_delete, name='vehicule_delete'),

    # --------------------------------------------------
    # 4. CRUD Conducteurs
    # --------------------------------------------------
    path('conducteurs/', views.conducteur_list, name='conducteur_list'),
    path('conducteurs/ajouter/', views.conducteur_create, name='conducteur_create'),
    path('conducteurs/modifier/<int:pk>/', views.conducteur_update, name='conducteur_update'),
    path('conducteurs/supprimer/<int:pk>/', views.conducteur_delete, name='conducteur_delete'),

    # --------------------------------------------------
    # 5. CRUD Affectations
    # --------------------------------------------------
    path('affectations/', views.affectation_list, name='affectation_list'),
    path('affectations/ajouter/', views.affectation_create, name='affectation_create'),
    path('affectations/modifier/<int:pk>/', views.affectation_update, name='affectation_update'),
    path('affectations/supprimer/<int:pk>/', views.affectation_delete, name='affectation_delete'),

    # --------------------------------------------------
    # 6. CRUD Rappels : Assurances (NOUVEAU)
    # --------------------------------------------------
    path('assurances/', views.assurance_list, name='assurance_list'),
    path('assurances/ajouter/', views.assurance_create, name='assurance_create'),
    path('assurances/modifier/<int:pk>/', views.assurance_update, name='assurance_update'),
    path('assurances/supprimer/<int:pk>/', views.assurance_delete, name='assurance_delete'),

    # --------------------------------------------------
    # 7. CRUD Rappels : Taxes de Circulation (NOUVEAU)
    # --------------------------------------------------
    path('taxes/', views.taxe_list, name='taxe_list'),
    path('taxes/ajouter/', views.taxe_create, name='taxe_create'),
    path('taxes/modifier/<int:pk>/', views.taxe_update, name='taxe_update'),
    path('taxes/supprimer/<int:pk>/', views.taxe_delete, name='taxe_delete'),

    # --------------------------------------------------
    # 8. CRUD Rappels : Visites Techniques (NOUVEAU)
    # --------------------------------------------------
    path('visites/', views.visite_list, name='visite_list'),
    path('visites/ajouter/', views.visite_create, name='visite_create'),
    path('visites/modifier/<int:pk>/', views.visite_update, name='visite_update'),
    path('visites/supprimer/<int:pk>/', views.visite_delete, name='visite_delete'),
]