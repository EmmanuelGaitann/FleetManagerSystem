from django.contrib import admin
from .models import Departement, Conducteur, Vehicule, Affectation

# 1. Gestion des Départements
@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'created_at')
    search_fields = ('nom',)

# 2. Gestion des Conducteurs
@admin.register(Conducteur)
class ConducteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'numero_permis', 'email', 'tel1', 'date_embauche')
    search_fields = ('nom', 'prenom', 'numero_permis')
    list_filter = ('ville', 'date_embauche')

# 3. Gestion des Véhicules
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'marque', 'modele', 'departement', 'actif', 'kilometrage_initial')
    search_fields = ('matricule', 'marque', 'modele', 'numero_serie')
    list_filter = ('actif', 'type_vehicule', 'type_carburant', 'departement')
    fieldsets = (
        ('Informations Générales', {
            'fields': ('matricule', 'marque', 'modele', 'couleur', 'numero_serie', 'departement', 'actif')
        }),
        ('Détails Achat / Location', {
            'fields': ('location_oui_non', 'date_achat_location', 'prix_achat_location', 'expiration_garantie', 'prix_vente', 'kilometrage_initial', 'note'),
            'classes': ('collapse',), # Masque cette section par défaut
        }),
    )

# 4. Gestion des Affectations (Historique Conducteur/Véhicule)
@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'conducteur', 'date_debut', 'date_fin')
    list_filter = ('vehicule', 'conducteur')
    raw_id_fields = ('vehicule', 'conducteur') # Utiliser une boîte de dialogue de recherche pour les FK