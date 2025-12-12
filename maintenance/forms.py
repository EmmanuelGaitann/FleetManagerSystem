# maintenance/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Entretien, DetailDepense, Assurance, TaxeCirculation, VisiteTechnique
# Importez les modèles externes nécessaires
from flotte.models import Vehicule, Conducteur
from fournisseurs.models import Fournisseur

# ==========================================================
# 1. Formulaire Ligne de Dépense (Base pour le Formset)
# ==========================================================

class DetailDepenseForm(forms.ModelForm):
    # Rendre ces champs obligatoires car ils sont essentiels pour le coût
    quantite = forms.IntegerField(min_value=1, label="Quantité")
    cout_unitaire = forms.DecimalField(min_value=0.01, decimal_places=2, label="Coût Unitaire (€)")

    class Meta:
        model = DetailDepense
        # Exclure 'entretien' car il sera géré par le Formset
        fields = ['description', 'quantite', 'cout_unitaire', 'piece']
        labels = {
            'piece': 'Pièce (Référence Fournisseur)',
            'description': "Description (Main d'œuvre, Autre)",
        }

# ==========================================================
# 2. Formulaire Principal d'Entretien
# ==========================================================

class EntretienForm(forms.ModelForm):
    # Assurez-vous que le champ ForeignKey 'fournisseur' filtre les prestataires de services
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtre pour n'afficher que les fournisseurs pertinents pour l'entretien/réparation
        try:
            self.fields['fournisseur'].queryset = Fournisseur.objects.filter(
                type_activite__in=['entretien', 'reparation']
            ).order_by('nom')
        except Exception:
            # Fallback si les rôles n'existent pas encore
            self.fields['fournisseur'].queryset = Fournisseur.objects.all().order_by('nom')

        # Rendre le champ Vehicule obligatoire et améliorer son label
        self.fields['vehicule'].label = 'Véhicule (Matricule)'

        # Rendre le champ fournisseur non obligatoire si c'est de l'auto-entretien
        self.fields['fournisseur'].required = False


    class Meta:
        model = Entretien
        fields = [
            'vehicule', 'fournisseur', 'date_entretien', 'kilometrage',
            'description', 'depense_type', 'entretien_maitre'
        ]
        widgets = {
            'date_entretien': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'depense_type': 'Type de Dépense (Ex: Vidange, Réparation)',
            'entretien_maitre': "Plan d'Entretien (Optionnel)",
        }

# ==========================================================
# 3. Formset Ligne de Dépense (Le cœur de la fonctionnalité)
# ==========================================================

DetailDepenseFormSet = inlineformset_factory(
    Entretien,                # Parent Model
    DetailDepense,            # Enfant Model (Ligne de dépense)
    form=DetailDepenseForm,   # Formulaire à utiliser pour chaque ligne
    extra=1,                  # Nombre de formulaires vides à afficher initialement
    can_delete=True           # Permettre la suppression des lignes existantes
)


# ==========================================================
# 4. Formulaires CRUD simples (Rappels)
# (A utiliser dans les vues ultérieures)
# ==========================================================

class AssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance
        fields = ['vehicule', 'fournisseur', 'date_assurance', 'expiration_assurance', 'rappel_avant_jours', 'note']
        widgets = {
            'date_assurance': forms.DateInput(attrs={'type': 'date'}),
            'expiration_assurance': forms.DateInput(attrs={'type': 'date'}),
        }

class TaxeCirculationForm(forms.ModelForm):
    class Meta:
        model = TaxeCirculation
        fields = ['vehicule', 'date_taxe_circulation', 'expiration', 'rappel_avant_jours', 'note']
        widgets = {
            'date_taxe_circulation': forms.DateInput(attrs={'type': 'date'}),
            'expiration': forms.DateInput(attrs={'type': 'date'}),
        }

class VisiteTechniqueForm(forms.ModelForm):
    class Meta:
        model = VisiteTechnique
        fields = ['vehicule', 'derniere_visite', 'prochaine_visite', 'rappel_avant_jours', 'note']
        widgets = {
            'derniere_visite': forms.DateInput(attrs={'type': 'date'}),
            'prochaine_visite': forms.DateInput(attrs={'type': 'date'}),
        }