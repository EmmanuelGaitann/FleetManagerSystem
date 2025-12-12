# FMS_Core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Redirige la racine vers le dashboard (qui déclenchera le login)
    # AJOUT du nom 'dashboard' pour que LOGIN_REDIRECT_URL fonctionne
    path('', lambda request: redirect('dashboard'), name='dashboard'),

    path('admin/', admin.site.urls),

    # URLs d'authentification de Django (login/logout).
    # Ces URLS sont : /auth/login/ (name='login'), /auth/logout/ (name='logout'), etc.
    path('auth/', include('django.contrib.auth.urls')),

    # URLS de notre application principale pour le web
    path('', include('flotte.urls')),
    path('', include('fournisseurs.urls')),
    path('', include('carburant.urls')),

    # --- AJOUT : Gestion des Utilisateurs ---
    path('utilisateurs/', include('utilisateurs.urls')),
    # --- AJOUT : Gestion de la Maintenance ---
    path('', include('maintenance.urls')), # Le chemin est vide pour les URLs 'entretiens/'

    # --- AJOUT : Gestion des Utilisateurs --
    path('utilisateurs/', include('utilisateurs.urls')),
]