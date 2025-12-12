# carburant/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F # NOUVEL IMPORT pour le calcul en BDD
from flotte.views import role_required

from .models import Ravitaillement
from .forms import RavitaillementForm


# -----------------------------------------------------------
# Vues CRUD du Module Carburant
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def ravitaillement_list(request):
    """Liste de tous les ravitaillements avec calcul du coût total."""
    # Utilisation de .annotate pour calculer total_depense_calc = quantite_litres * prix_unitaire
    ravitaillements = Ravitaillement.objects.select_related('vehicule', 'fournisseur').annotate(
        total_depense_calc=F('quantite_litres') * F('prix_unitaire')
    ).order_by('-date_plein')

    context = {
        'ravitaillements': ravitaillements,
        'title': 'Liste des Ravitaillements'
    }
    return render(request, 'carburant/ravitaillement_list.html', context)

@role_required('Gestionnaire Flotte')
def ravitaillement_create(request):
    """Ajout d'un nouveau ravitaillement."""
    if request.method == 'POST':
        form = RavitaillementForm(request.POST)
        if form.is_valid():
            form.save() # Le total_depense n'est plus géré ici
            return redirect('ravitaillement_list')
    else:
        form = RavitaillementForm()

    context = {
        'form': form,
        'title': 'Enregistrer un Ravitaillement',
        'action': 'Enregistrer'
    }
    return render(request, 'carburant/ravitaillement_form.html', context)

@role_required('Gestionnaire Flotte')
def ravitaillement_update(request, pk):
    """Modification d'un ravitaillement existant."""
    ravitaillement = get_object_or_404(Ravitaillement, pk=pk)
    if request.method == 'POST':
        form = RavitaillementForm(request.POST, instance=ravitaillement)
        if form.is_valid():
            form.save()
            return redirect('ravitaillement_list')
    else:
        form = RavitaillementForm(instance=ravitaillement)

    context = {
        'form': form,
        'title': 'Modifier le Ravitaillement',
        'action': 'Sauvegarder'
    }
    return render(request, 'carburant/ravitaillement_form.html', context)


@role_required('Gestionnaire Flotte')
def ravitaillement_delete(request, pk):
    """Suppression d'un ravitaillement."""
    ravitaillement = get_object_or_404(Ravitaillement, pk=pk)
    if request.method == 'POST':
        ravitaillement.delete()
        return redirect('ravitaillement_list')

    context = {
        'ravitaillement': ravitaillement,
        'title': 'Supprimer le Ravitaillement'
    }
    return render(request, 'carburant/ravitaillement_confirm_delete.html', context)