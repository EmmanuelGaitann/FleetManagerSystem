from django.contrib import admin
from .models import Carburant, EntretienMaitre, Entretien, Assurance, TaxeCirculation, VisiteTechnique, Anomalie, AlerteEmail

# 1. Gestion des Plans d'Entretien (Entretien Maître)
@admin.register(EntretienMaitre)
class EntretienMaitreAdmin(admin.ModelAdmin):
    list_display = ('description', 'repeter_par_date', 'repeter_par_kilometrage')
    search_fields = ('description',)

# 2. Gestion des Entretien effectués (Historique)
class DetailDepenseInline(admin.TabularInline):
    # Ce modèle n'est pas créé ici, mais doit être importé si vous le souhaitez
    # from .models import DetailDepense # A ajouter en haut du fichier
    # model = DetailDepense
    # extra = 1
    pass

@admin.register(Entretien)
class EntretienAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'date_entretien', 'kilometrage', 'cout_total', 'depense_type')
    search_fields = ('vehicule__matricule', 'description')
    list_filter = ('depense_type', 'fournisseur')
    raw_id_fields = ('vehicule', 'fournisseur', 'entretien_maitre')
    # inlines = [DetailDepenseInline] # Ajouter l'inline pour les détails

# 3. Gestion des Pleins de Carburant
@admin.register(Carburant)
class CarburantAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'date_plein', 'quantite', 'prix_unitaire', 'kilometrage', 'station_service')
    search_fields = ('vehicule__matricule', 'station_service')
    list_filter = ('fournisseur',)
    raw_id_fields = ('vehicule', 'fournisseur')

# 4. Gestion des Assurances
@admin.register(Assurance)
class AssuranceAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'date_assurance', 'expiration_assurance', 'rappel_avant_jours', 'fournisseur')
    list_filter = ('fournisseur',)
    raw_id_fields = ('vehicule', 'fournisseur')

# 5. Gestion des Taxes
@admin.register(TaxeCirculation)
class TaxeCirculationAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'date_taxe_circulation', 'expiration', 'rappel_avant_jours')
    raw_id_fields = ('vehicule',)

# 6. Gestion des Visites Techniques
@admin.register(VisiteTechnique)
class VisiteTechniqueAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'derniere_visite', 'prochaine_visite', 'rappel_avant_jours')
    raw_id_fields = ('vehicule',)

# 7. Gestion des Anomalies (Déclarations)
@admin.register(Anomalie)
class AnomalieAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'conducteur', 'type_anomalie', 'statut', 'date_declaration')
    list_filter = ('statut', 'type_anomalie')
    search_fields = ('vehicule__matricule', 'conducteur__nom', 'description')
    raw_id_fields = ('vehicule', 'conducteur')

# 8. Gestion des Alertes E-mail
@admin.register(AlerteEmail)
class AlerteEmailAdmin(admin.ModelAdmin):
    list_display = ('email_destinataire', 'type_alerte')
    list_filter = ('type_alerte',)