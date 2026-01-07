# rapports/forms.py
from django import forms
from .models import SimulationTrajet


class SimulationTrajetForm(forms.ModelForm):
    """
    Formulaire pour la simulation de trajet.
    Deux modes possibles :
    - Soit on saisit tout à la main (distance, conso, prix).
    - Soit plus tard tu pourras brancher une API pour calculer automatiquement distance/durée.
    """
    prix_carburant_litre = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        initial=850,
        label="Prix du carburant (XAF / Litre)",
        help_text="Utilisé pour estimer le coût du trajet."
    )

    utiliser_algo_simple = forms.BooleanField(
        required=False,
        initial=True,
        label="Utiliser l'algorithme simple (distance × conso)",
        help_text="Si décoché, tu pourras plus tard brancher une API externe."
    )

    class Meta:
        model = SimulationTrajet
        fields = [
            'vehicule',
            'point_depart',
            'point_arrivee',
            'distance_km',
            'duree_minutes',
            'consommation_moyenne_l_100',
        ]
        widgets = {
            'point_depart': forms.TextInput(attrs={'class': 'form-control'}),
            'point_arrivee': forms.TextInput(attrs={'class': 'form-control'}),
            'distance_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duree_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'consommation_moyenne_l_100': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vehicule': forms.Select(attrs={'class': 'form-select'}),
        }
