# maintenance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # CRUD Entretien (Avec Formset)
    path('entretiens/', views.entretien_list, name='entretien_list'),
    path('entretiens/ajouter/', views.entretien_create, name='entretien_create'),
    path('entretiens/modifier/<int:pk>/', views.entretien_update, name='entretien_update'),
    path('entretiens/supprimer/<int:pk>/', views.entretien_delete, name='entretien_delete'),

    # NOUVEAU : CRUD Anomalie (Déclarations)
    path('anomalies/', views.anomalie_list, name='anomalie_list'),
    path('anomalies/declarer/', views.anomalie_create, name='anomalie_create'),
    path('anomalies/details/<int:pk>/', views.anomalie_detail, name='anomalie_detail'),
    path('anomalies/modifier/<int:pk>/', views.anomalie_update, name='anomalie_update'),
    path('anomalies/supprimer/<int:pk>/', views.anomalie_delete, name='anomalie_delete'),
    path('mes-anomalies/', views.mes_anomalies, name='mes_anomalies'),
    path('plan-entretien/', views.plan_entretien, name='plan_entretien'),
]