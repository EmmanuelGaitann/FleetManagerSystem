# rapports/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rapports principaux
    path('tco/', views.rapports_tco, name='rapports_tco'),
    path('performance-carburant/', views.rapports_performance, name='rapports_performance'),
    # Alertes
    path('alertes-actives/', views.alerte_list, name='alerte_list'),
    # Simulation de trajet (Module 5)
    path('simulation-trajet/', views.simulation_trajet, name='simulation_trajet'),
    path("alertes-echeances/", views.alertes_echeances, name="alertes_echeances"),
    path('utilisation/', views.rapports_utilisation, name='rapports_utilisation'),
    path('anomalies/', views.rapports_anomalies, name='rapports_anomalies'),
    path('utilisation/export-csv/', views.export_utilisation_csv, name='export_utilisation_csv'),
    path('anomalies/export-csv/', views.export_anomalies_csv, name='export_anomalies_csv'),



]