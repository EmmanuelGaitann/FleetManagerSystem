from django.contrib import admin
from .models import Fournisseur, Piece

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_activite', 'ville', 'tel1', 'email')
    search_fields = ('nom', 'type_activite', 'ville')
    list_filter = ('type_activite',)

@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'numero', 'constructeur', 'prix', 'fournisseur', 'date_prix')
    search_fields = ('nom', 'numero', 'constructeur')
    list_filter = ('fournisseur', 'constructeur')
    raw_id_fields = ('fournisseur',)