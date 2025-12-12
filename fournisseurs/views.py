# fournisseurs/views.py (Contenu complet avec les vues Pièce ajoutées)

from django.shortcuts import render, redirect, get_object_or_404
from flotte.views import role_required # Import du décorateur

from .models import Fournisseur, Piece # S'assurer que Piece est importé
from .forms import FournisseurForm, PieceForm # S'assurer que PieceForm est importé


# -----------------------------------------------------------
# Vues CRUD du Module Fournisseurs (EXISTANTES)
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def fournisseur_list(request):
    """Liste de tous les fournisseurs."""
    fournisseurs = Fournisseur.objects.all().order_by('nom')
    context = {
        'fournisseurs': fournisseurs,
        'title': 'Liste des Fournisseurs'
    }
    return render(request, 'fournisseurs/fournisseur_list.html', context)

@role_required('Gestionnaire Flotte')
def fournisseur_create(request):
    """Ajout d'un nouveau fournisseur."""
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fournisseur_list')
    else:
        form = FournisseurForm()

    context = {
        'form': form,
        'title': 'Ajouter un Fournisseur',
        'action': 'Créer'
    }
    return render(request, 'fournisseurs/fournisseur_form.html', context)

@role_required('Gestionnaire Flotte')
def fournisseur_update(request, pk):
    """Modification d'un fournisseur existant."""
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect('fournisseur_list')
    else:
        # Passage du type_activite initial pour le formulaire ChoiceField (si vous en avez un)
        # Note : Si vous n'utilisez pas de ChoiceField, retirez cette ligne.
        initial_data = {'type_activite': fournisseur.type_activite}
        form = FournisseurForm(instance=fournisseur, initial=initial_data) # Retire 'initial=initial_data' si vous n'en avez pas besoin.

    context = {
        'form': form,
        'title': 'Modifier le Fournisseur',
        'action': 'Sauvegarder'
    }
    return render(request, 'fournisseurs/fournisseur_form.html', context)


@role_required('Gestionnaire Flotte')
def fournisseur_delete(request, pk):
    """Suppression d'un fournisseur."""
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    if request.method == 'POST':
        fournisseur.delete()
        return redirect('fournisseur_list')

    context = {
        'fournisseur': fournisseur,
        'title': 'Supprimer le Fournisseur'
    }
    return render(request, 'fournisseurs/fournisseur_confirm_delete.html', context)


# -----------------------------------------------------------
# Vues CRUD du Module Pièces (NOUVEAU)
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def piece_list(request):
    """Liste de toutes les pièces."""
    pieces = Piece.objects.select_related('fournisseur').all().order_by('nom')
    context = {
        'pieces': pieces,
        'title': 'Catalogue des Pièces'
    }
    return render(request, 'fournisseurs/piece_list.html', context)

@role_required('Gestionnaire Flotte')
def piece_create(request):
    """Ajout d'une nouvelle pièce."""
    if request.method == 'POST':
        form = PieceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('piece_list')
    else:
        form = PieceForm()

    context = {
        'form': form,
        'title': 'Ajouter une Pièce',
        'action': 'Créer'
    }
    return render(request, 'fournisseurs/piece_form.html', context)

@role_required('Gestionnaire Flotte')
def piece_update(request, pk):
    """Modification d'une pièce existante."""
    piece = get_object_or_404(Piece, pk=pk)
    if request.method == 'POST':
        form = PieceForm(request.POST, instance=piece)
        if form.is_valid():
            form.save()
            return redirect('piece_list')
    else:
        form = PieceForm(instance=piece)

    context = {
        'form': form,
        'title': 'Modifier la Pièce',
        'action': 'Sauvegarder'
    }
    return render(request, 'fournisseurs/piece_form.html', context)


@role_required('Gestionnaire Flotte')
def piece_delete(request, pk):
    """Suppression d'une pièce."""
    piece = get_object_or_404(Piece, pk=pk)
    if request.method == 'POST':
        piece.delete()
        return redirect('piece_list')

    context = {
        'piece': piece,
        'title': 'Supprimer la Pièce'
    }
    return render(request, 'fournisseurs/piece_confirm_delete.html', context)