# maintenance/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction # NÉCESSAIRE pour garantir l'intégrité (Entretien + Détails)
from django.db.models import Sum, F
from flotte.views import role_required # Votre décorateur de sécurité
from .models import Entretien, DetailDepense
from .forms import EntretienForm, DetailDepenseFormSet

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