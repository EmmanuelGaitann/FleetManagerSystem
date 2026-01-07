# maintenance/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction # NÉCESSAIRE pour garantir l'intégrité (Entretien + Détails)
from django.db.models import Sum, F
from flotte.views import role_required # Votre décorateur de sécurité
from .models import Entretien, DetailDepense, Anomalie
from .forms import EntretienForm, DetailDepenseFormSet, AnomalieForm
from django.utils import timezone


# -----------------------------------------------------------
# Vues CRUD du Module Entretien (Avec Formset)
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def entretien_list(request):
    """Liste de tous les entretiens avec calcul du coût total."""
    # Annoter chaque entretien avec la somme de ses DetailDepense
    entretiens = Entretien.objects.select_related('vehicule', 'fournisseur').annotate(
        # Calcul du coût total à la volée: SUM(quantite * cout_unitaire)
        cout_calcule=Sum(F('detaildepense__quantite') * F('detaildepense__cout_unitaire'))
    ).order_by('-date_entretien')

    context = {
        'entretiens': entretiens,
        'title': 'Historique des Entretiens'
    }
    return render(request, 'maintenance/entretien_list.html', context)


@role_required('Gestionnaire Flotte')
def entretien_create(request):
    """Ajout d'un nouvel entretien avec ses lignes de dépenses."""
    if request.method == 'POST':
        form = EntretienForm(request.POST)
        formset = DetailDepenseFormSet(request.POST, instance=Entretien())

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # 1. Sauvegarde l'entretien principal (ne pas encore commit)
                entretien = form.save(commit=False)
                # Calcule le coût total (important pour le champ 'cout_total' du modèle Entretien)

                # Sauvegarde l'entretien dans la BDD
                entretien.save()

                # 2. Associe l'entretien aux lignes de dépenses et les sauvegarde
                formset.instance = entretien
                formset.save()

                # Mettre à jour le champ cout_total sur l'objet Entretien (après la sauvegarde du Formset)
                total_depense = entretien.detaildepense_set.aggregate(
                    total=Sum(F('quantite') * F('cout_unitaire'))
                )['total'] or 0.00 # Utiliser 0.00 si aucune dépense n'est enregistrée

                entretien.cout_total = total_depense
                entretien.save(update_fields=['cout_total'])

            return redirect('entretien_list')
    else:
        form = EntretienForm()
        formset = DetailDepenseFormSet(instance=Entretien()) # Instance vide pour la création

    context = {
        'form': form,
        'formset': formset,
        'title': 'Ajouter un Entretien',
        'action': 'Créer'
    }
    # Le template doit être créé : maintenance/entretien_form.html
    return render(request, 'maintenance/entretien_form.html', context)


@role_required('Gestionnaire Flotte')
def entretien_update(request, pk):
    """Modification d'un entretien existant avec ses lignes de dépenses."""
    entretien = get_object_or_404(Entretien, pk=pk)

    if request.method == 'POST':
        form = EntretienForm(request.POST, instance=entretien)
        formset = DetailDepenseFormSet(request.POST, instance=entretien)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # 1. Sauvegarde l'entretien principal
                entretien = form.save()

                # 2. Sauvegarde ou met à jour les lignes de dépenses (DetailDepense)
                formset.save()

                # 3. Recalcule et met à jour le champ cout_total
                total_depense = entretien.detaildepense_set.aggregate(
                    total=Sum(F('quantite') * F('cout_unitaire'))
                )['total'] or 0.00

                entretien.cout_total = total_depense
                entretien.save(update_fields=['cout_total'])

            return redirect('entretien_list')
    else:
        form = EntretienForm(instance=entretien)
        formset = DetailDepenseFormSet(instance=entretien) # Charge les lignes de dépenses existantes

    context = {
        'form': form,
        'formset': formset,
        'title': 'Modifier l\'Entretien',
        'action': 'Sauvegarder'
    }
    return render(request, 'maintenance/entretien_form.html', context)

@role_required('Gestionnaire Flotte')
def entretien_delete(request, pk):
    """Suppression d'un entretien."""
    entretien = get_object_or_404(Entretien, pk=pk)
    if request.method == 'POST':
        entretien.delete()
        return redirect('entretien_list')
    context = {
        'entretien': entretien,
        'title': 'Supprimer l\'Entretien'
    }
    # Le template doit être créé : maintenance/entretien_confirm_delete.html
    return render(request, 'maintenance/entretien_confirm_delete.html', context)

# -----------------------------------------------------------
# Vues CRUD du Module Anomalie
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte', 'Chauffeur/Opérateur')
def anomalie_list(request):
    """Liste de toutes les anomalies."""
    anomalies = Anomalie.objects.select_related('vehicule', 'conducteur').order_by('-date_declaration')

    context = {
        'anomalies': anomalies,
        'title': 'Liste des Anomalies Déclarées'
    }
    # Le template doit être créé : maintenance/anomalie_list.html
    return render(request, 'maintenance/anomalie_list.html', context)


@role_required('Gestionnaire Flotte', 'Chauffeur/Opérateur')
def anomalie_create(request):
    """Déclaration d'une nouvelle anomalie."""
    if request.method == 'POST':
        form = AnomalieForm(request.POST)
        if form.is_valid():
            anomalie = form.save(commit=False)
            # Définir le statut et la date au moment de la déclaration
            anomalie.statut = 'Signalé'
            anomalie.date_declaration = timezone.now() # Nécessite d'importer timezone

            anomalie.save()
            return redirect('anomalie_list')
    else:
        form = AnomalieForm()

    context = {
        'form': form,
        'title': 'Déclarer une Anomalie',
        'action': 'Déclarer'
    }
    # Le template doit être créé : maintenance/anomalie_form.html
    return render(request, 'maintenance/anomalie_form.html', context)


@role_required('Gestionnaire Flotte')
def anomalie_update(request, pk):
    """Modification du statut ou des détails par un Gestionnaire Flotte."""
    anomalie = get_object_or_404(Anomalie, pk=pk)

    if request.method == 'POST':
        form = AnomalieForm(request.POST, instance=anomalie)
        if form.is_valid():
            form.save()
            return redirect('anomalie_list')
    else:
        form = AnomalieForm(instance=anomalie)

    context = {
        'form': form,
        'title': 'Mettre à jour l\'Anomalie',
        'action': 'Sauvegarder'
    }
    return render(request, 'maintenance/anomalie_form.html', context)


@role_required('Gestionnaire Flotte')
def anomalie_detail(request, pk):
    """Afficher les détails d'une anomalie (pour inspection/résolution)."""
    anomalie = get_object_or_404(Anomalie, pk=pk)

    context = {
        'anomalie': anomalie,
        'title': f'Détails Anomalie #{anomalie.id}'
    }
    # Le template doit être créé : maintenance/anomalie_detail.html
    return render(request, 'maintenance/anomalie_detail.html', context)


@role_required('Gestionnaire Flotte')
def anomalie_delete(request, pk):
    """Suppression d'une anomalie."""
    anomalie = get_object_or_404(Anomalie, pk=pk)
    if request.method == 'POST':
        anomalie.delete()
        return redirect('anomalie_list')

    context = {
        'anomalie': anomalie,
        'title': 'Supprimer l\'Anomalie'
    }
    # Le template doit être créé : maintenance/anomalie_confirm_delete.html
    return render(request, 'maintenance/anomalie_confirm_delete.html', context)