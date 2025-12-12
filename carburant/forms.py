# carburant/forms.py

from django import forms
from .models import Ravitaillement
from fournisseurs.models import Fournisseur

class RavitaillementForm(forms.ModelForm):
    date_plein = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Date et Heure du Plein"
    )

    class Meta:
        model = Ravitaillement
        # Les champs sont alignés sur le modèle corrigé (sans total_depense)
        fields = [
            'vehicule', 'fournisseur', 'date_plein', 'kilometrage',
            'quantite_litres', 'prix_unitaire'
        ]
        labels = {
            'quantite_litres': 'Quantité (Litres)',
            'prix_unitaire': 'Prix Unitaire',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrer le champ fournisseur
        try:
            self.fields['fournisseur'].queryset = Fournisseur.objects.filter(
                type_activite='vente_carburant'
            ).order_by('nom')
        except Exception:
            self.fields['fournisseur'].queryset = Fournisseur.objects.all().order_by('nom')

    # Les méthodes clean() et save() n'ont pas besoin d'être modifiées ou sont retirées
    # car elles ne gèrent plus le calcul et la sauvegarde du total_depense.
    pass