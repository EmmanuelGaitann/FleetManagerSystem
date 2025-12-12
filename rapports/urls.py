# rapports/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rapports principaux
    path('tco/', views.rapports_tco, name='rapports_tco'),
    path('performance-carburant/', views.rapports_performance, name='rapports_performance'),
    # Alertes
    path('alertes-actives/', views.alerte_list, name='alerte_list'),
]