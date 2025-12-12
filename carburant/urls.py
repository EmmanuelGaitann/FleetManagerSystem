# carburant/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # CRUD Ravitaillements
    path('ravitaillements/', views.ravitaillement_list, name='ravitaillement_list'),
    path('ravitaillements/ajouter/', views.ravitaillement_create, name='ravitaillement_create'),
    path('ravitaillements/modifier/<int:pk>/', views.ravitaillement_update, name='ravitaillement_update'),
    path('ravitaillements/supprimer/<int:pk>/', views.ravitaillement_delete, name='ravitaillement_delete'),
]