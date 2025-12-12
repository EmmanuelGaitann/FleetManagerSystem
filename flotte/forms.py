from django import forms
from django.db import models
# Import de TOUS les modèles nécessaires, y compris les nouveaux rappels
from .models import (
    Departement, Vehicule, Conducteur, Affectation,
    Assurance, TaxeCirculation, VisiteTechnique
)

# ==========================================================
# 1. Formulaire Département (Existant)
# ==========================================================

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom']


# ==========================================================
# 2. Formulaire Véhicule (RÉVISÉ pour votre BDD)
# ==========================================================

class VehiculeForm(forms.ModelForm):
    # Les champs 'actif' et 'location_oui_non' sont des IntegerField (0/1) dans la BDD.
    # Nous les représentons comme des BooleanField dans le formulaire pour une meilleure UX.
    actif = forms.BooleanField(required=False, label='Véhicule actif')
    location_oui_non = forms.BooleanField(required=False, label='Véhicule en location')

    class Meta:
        model = Vehicule
        # Utilisez les noms de champs exacts de votre modèle
        fields = [
            'matricule', 'marque', 'modele', 'couleur', 'numero_serie',
            'date_mise_circulation', 'type_vehicule', 'type_carburant',
            'kilometrage_initial', 'actif', 'departement',
            'location_oui_non', 'date_achat_location', 'prix_achat_location',
            'expiration_garantie', 'prix_vente', 'note'
        ]
        labels = {
            'numero_serie': 'Numéro de Série',
            'date_mise_circulation': 'Date de Mise en Circulation',
            'type_vehicule': 'Type de Véhicule',
            'type_carburant': 'Type de Carburant',
            'kilometrage_initial': 'Kilométrage Initial',
            'date_achat_location': "Date d'Achat/Location",
            'prix_achat_location': "Prix d'Achat/Location",
        }
        widgets = {
            'date_mise_circulation': forms.DateInput(attrs={'type': 'date'}),
            'date_achat_location': forms.DateInput(attrs={'type': 'date'}),
            'expiration_garantie': forms.DateInput(attrs={'type': 'date'}),
        }

    # Surcharge de la méthode save pour convertir les booléens en 0/1 pour la base de données
    def save(self, commit=True):
        instance = super().save(commit=False)

        # Conversion du BooleanField du formulaire en Integer (0 ou 1) pour le modèle
        instance.actif = 1 if self.cleaned_data.get('actif') else 0
        instance.location_oui_non = 1 if self.cleaned_data.get('location_oui_non') else 0

        if commit:
            instance.save()
        return instance


# ==========================================================
# 3. Formulaire Conducteur (Existant)
# ==========================================================

class ConducteurForm(forms.ModelForm):
    class Meta:
        model = Conducteur
        fields = [
            'nom', 'prenom', 'date_naissance', 'date_embauche',
            'numero_permis', 'adresse', 'ville', 'tel1', 'tel2', 'email'
        ]
        labels = {
            'date_naissance': 'Date de Naissance',
            'date_embauche': "Date d'Embauche",
            'numero_permis': 'Numéro de Permis',
            'tel1': 'Téléphone 1',
            'tel2': 'Téléphone 2',
        }
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'placeholder': 'nom@exemple.com'}),
        }


# ==========================================================
# 4. Formulaire Affectation (Existant)
# ==========================================================

class AffectationForm(forms.ModelForm):
    class Meta:
        model = Affectation
        fields = ['vehicule', 'conducteur', 'date_debut', 'date_fin']
        labels = {
            'date_debut': 'Date de Début',
            'date_fin': 'Date de Fin (Laisser vide si en cours)',
        }
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'required': False}),
        }

    def clean(self):
        cleaned_data = super().clean()
        vehicule = cleaned_data.get('vehicule')
        conducteur = cleaned_data.get('conducteur')
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        # 1. Vérification des dates
        if date_debut and date_fin and date_fin < date_debut:
            self.add_error('date_fin', "La date de fin ne peut pas être antérieure à la date de début de l'affectation.")

        # 2. Vérification des conflits (Un seul véhicule/conducteur affecté à la fois)
        instance = getattr(self, 'instance', None)

        # Trouver les affectations ouvertes (date_fin IS NULL) pour le véhicule OU le conducteur
        open_assignments = Affectation.objects.filter(
            models.Q(vehicule=vehicule) | models.Q(conducteur=conducteur),
            date_fin__isnull=True
        ).exclude(pk=instance.pk if instance else None)

        if open_assignments.exists():
            self.add_error(None, "Ce véhicule ou ce conducteur est déjà dans une affectation en cours (sans date de fin).")

        return cleaned_data

# ==========================================================
# 5. Formulaire Assurance (CORRIGÉ)
# ==========================================================

class AssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance
        fields = [
            'vehicule', 'fournisseur', 'date_assurance', 'expiration_assurance',
            'rappel_avant_jours', 'note'
        ]
        labels = {
            'fournisseur': 'Assureur',
            'date_assurance': 'Date de la Police',
            'expiration_assurance': "Date d'Expiration",
            'rappel_avant_jours': 'Rappel avant (jours)',
        }
        widgets = {
            'date_assurance': forms.DateInput(attrs={'type': 'date'}),
            'expiration_assurance': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }

# ==========================================================
# 6. Formulaire TaxeCirculation (CORRIGÉ)
# ==========================================================

class TaxeCirculationForm(forms.ModelForm):
    class Meta:
        model = TaxeCirculation
        fields = ['vehicule', 'date_taxe_circulation', 'expiration', 'rappel_avant_jours', 'note']
        labels = {
            'date_taxe_circulation': 'Date de la Taxe',
            'expiration': "Date d'Expiration",
            'rappel_avant_jours': 'Rappel avant (jours)',
        }
        widgets = {
            'date_taxe_circulation': forms.DateInput(attrs={'type': 'date'}),
            'expiration': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }

# ==========================================================
# 7. Formulaire VisiteTechnique (CORRIGÉ)
# ==========================================================

class VisiteTechniqueForm(forms.ModelForm):
    class Meta:
        model = VisiteTechnique
        fields = ['vehicule', 'derniere_visite', 'prochaine_visite', 'rappel_avant_jours', 'note']
        labels = {
            'derniere_visite': 'Date Dernière Visite',
            'prochaine_visite': 'Date Prochaine Visite',
            'rappel_avant_jours': 'Rappel avant (jours)',
        }
        widgets = {
            'derniere_visite': forms.DateInput(attrs={'type': 'date'}),
            'prochaine_visite': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }