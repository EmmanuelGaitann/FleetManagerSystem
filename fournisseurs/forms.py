# fournisseurs/forms.py (Ajout du PieceForm)

from django import forms
from .models import Fournisseur, Piece # S'assurer que Piece est importé

# Définition des choix d'activité pour le formulaire Fournisseur
ACTIVITE_CHOICES = [
    ('vente_vehicule', 'Vente de Véhicules'),
    ('location_vehicule', 'Location de Véhicules'),
    ('assureur', 'Assureur'),
    ('vente_piece_auto', 'Vente de Pièces Auto'),
    ('entretien', 'Entretien et Réparation'),
    ('reparation', 'Réparation'),
    ('vente_carburant', 'Vente de Carburant'),
    ('autre', 'Autre'),
]

# ==========================================================
# 1. Formulaire Fournisseur (Version complète)
# ==========================================================

class FournisseurForm(forms.ModelForm):
    type_activite = forms.ChoiceField(
        choices=ACTIVITE_CHOICES,
        label="Type d'Activité"
    )

    class Meta:
        model = Fournisseur
        fields = [
            'nom', 'type_activite', 'contact', 'tel1', 'tel2', 'ville',
            'site_web', 'email', 'type_fournisseur'
        ]
        widgets = {
            'site_web': forms.URLInput(attrs={'placeholder': 'https://www.exemple.com'}),
            'email': forms.EmailInput(attrs={'placeholder': 'contact@exemple.com'}),
        }

# ==========================================================
# 2. Formulaire Pièce (NOUVEAU)
# ==========================================================

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = [
            'fournisseur', 'constructeur', 'numero', 'nom', 'prix', 'date_prix'
        ]
        labels = {
            'constructeur': 'Constructeur de la pièce',
            'numero': 'Numéro de la Pièce',
            'nom': 'Nom Commercial',
            'prix': 'Prix Unitaire (€)',
            'date_prix': 'Date du Prix (Dernière MàJ)',
        }
        widgets = {
            'date_prix': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les fournisseurs pour n'afficher que ceux de type 'vente_piece_auto'
        try:
            self.fields['fournisseur'].queryset = Fournisseur.objects.filter(
                type_activite='vente_piece_auto'
            ).order_by('nom')
        except Exception:
            self.fields['fournisseur'].queryset = Fournisseur.objects.all().order_by('nom')