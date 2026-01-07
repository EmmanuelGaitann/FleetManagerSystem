from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta

from flotte.views import role_required
from .models import Entretien, DetailDepense, Anomalie, EntretienMaitre
from .forms import EntretienForm, DetailDepenseFormSet, AnomalieForm
from carburant.models import Ravitaillement
from flotte.models import Conducteur, Affectation


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
                # 1. Sauvegarde l'entretien principal SANS le formset
                entretien = form.save(commit=False)

                # IMPORTANT : donner une valeur initiale à cout_total
                # pour respecter la contrainte NOT NULL en base
                entretien.cout_total = 0
                entretien.save()  # première sauvegarde OK

                # 2. Associer l'entretien aux lignes de dépenses et les sauvegarder
                formset.instance = entretien
                formset.save()

                # 3. Recalculer le coût total à partir des lignes de dépenses
                total_depense = entretien.detaildepense_set.aggregate(
                    total=Sum(F('quantite') * F('cout_unitaire'))
                )['total'] or 0.00  # 0 si aucune dépense

                entretien.cout_total = total_depense
                entretien.save(update_fields=['cout_total'])

            return redirect('entretien_list')
    else:
        form = EntretienForm()
        formset = DetailDepenseFormSet(instance=Entretien())  # Instance vide pour la création

    context = {
        'form': form,
        'formset': formset,
        'title': "Ajouter un Entretien",
        'action': 'Sauvegarder'
    }
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

@role_required('Chauffeur/Opérateur')
def mes_anomalies(request):
    """
    Espace chauffeur :
    - Affiche les anomalies déclarées par le chauffeur connecté
    - Permet de déclarer une nouvelle anomalie sur le véhicule actuellement affecté
    """

    user = request.user
    conducteur = Conducteur.objects.filter(email=user.email).first()

    today = timezone.now().date()
    affectation_actuelle = None

    if conducteur:
        # Même logique que dans mes_affectations : d'abord sans date_fin, puis avec
        affectation_actuelle = (
            Affectation.objects
            .filter(
                conducteur=conducteur,
                date_debut__lte=today,
                date_fin__isnull=True
            )
            .select_related('vehicule')
            .order_by('-date_debut')
            .first()
        )
        if not affectation_actuelle:
            affectation_actuelle = (
                Affectation.objects
                .filter(
                    conducteur=conducteur,
                    date_debut__lte=today,
                    date_fin__gte=today
                )
                .select_related('vehicule')
                .order_by('-date_debut')
                .first()
            )

    # Historique des anomalies du chauffeur
    anomalies = []
    if conducteur:
        anomalies = (
            Anomalie.objects
            .filter(conducteur=conducteur)
            .select_related('vehicule')
            .order_by('-date_declaration')
        )

    message_error = None

    if request.method == 'POST':
        if not conducteur:
            message_error = "Aucun profil chauffeur n'est associé à ce compte."
        elif not affectation_actuelle:
            message_error = "Aucun véhicule ne vous est actuellement affecté : vous ne pouvez pas déclarer d'anomalie."
        else:
            type_anomalie = request.POST.get('type_anomalie') or ''
            description = request.POST.get('description') or ''
            photo_path = request.POST.get('photo_path') or ''

            if not description.strip():
                message_error = "La description de l'anomalie est obligatoire."
            else:
                Anomalie.objects.create(
                    vehicule=affectation_actuelle.vehicule,
                    conducteur=conducteur,
                    type_anomalie=type_anomalie,
                    description=description,
                    statut='Signalé',
                    date_declaration=timezone.now(),
                    photo_path=photo_path
                )
                return redirect('mes_anomalies')

    context = {
        'conducteur': conducteur,
        'affectation_actuelle': affectation_actuelle,
        'anomalies': anomalies,
        'message_error': message_error,
        'title': "Mes anomalies",
    }
    return render(request, 'maintenance/mes_anomalies.html', context)

@role_required('Gestionnaire Flotte')
def plan_entretien(request):
    """
    Plan d'entretien & rappels :
    - Pour chaque véhicule + plan d'entretien (EntretienMaitre),
      on calcule la prochaine échéance par DATE et / ou par KM.
    - Si l'échéance est proche (ou déjà dépassée), on l'affiche.
    """

    today = timezone.now().date()

    DEFAULT_RAPPEL_JOURS = 30    # si rappel non renseigné sur le plan
    DEFAULT_RAPPEL_KM = 1000     # idem pour le km

    # 1) On récupère les DERNIERS entretiens par (véhicule, plan)
    #    avec un dictionnaire
    entretiens = (
        Entretien.objects
        .select_related('vehicule', 'entretien_maitre')
        .exclude(entretien_maitre__isnull=True)
        .order_by('vehicule_id', 'entretien_maitre_id', 'date_entretien')
    )

    derniers = {}  # key: (vehicule_id, plan_id) -> entretien le plus récent
    for e in entretiens:
        key = (e.vehicule_id, e.entretien_maitre_id)
        derniers[key] = e  # comme on est trié par date, la dernière occurrence reste

    lignes_date = []
    lignes_km = []

    for (veh_id, plan_id), entretien in derniers.items():
        plan = entretien.entretien_maitre
        vehicule = entretien.vehicule

        # ------------------------------
        # A) Plan basé sur la DATE
        # ------------------------------
        if plan.repeter_par_date:
            prochaine_date = entretien.date_entretien + timedelta(days=plan.repeter_par_date)
            jours_restants = (prochaine_date - today).days
            rappel_jours = plan.rappel_avant_jours or DEFAULT_RAPPEL_JOURS

            # On affiche si l'échéance est dans la fenêtre de rappel (ou déjà passée)
            if jours_restants <= rappel_jours:
                lignes_date.append({
                    'vehicule': vehicule,
                    'plan': plan,
                    'dernier_entretien': entretien,
                    'prochaine_date': prochaine_date,
                    'jours_restants': jours_restants,
                    'en_retard': jours_restants < 0,
                })

        # ------------------------------
        # B) Plan basé sur le KILOMÉTRAGE
        # ------------------------------
        if plan.repeter_par_kilometrage:
            # km actuel = dernier plein, sinon dernier entretien
            last_rav = (
                Ravitaillement.objects
                .filter(vehicule=vehicule)
                .order_by('-date_plein')
                .first()
            )

            if last_rav and last_rav.kilometrage is not None:
                km_actuel = last_rav.kilometrage
            else:
                km_actuel = entretien.kilometrage

            prochain_km = entretien.kilometrage + plan.repeter_par_kilometrage
            km_restants = prochain_km - km_actuel
            rappel_km = plan.rappel_avant_kilometrage or DEFAULT_RAPPEL_KM

            if km_restants <= rappel_km:
                lignes_km.append({
                    'vehicule': vehicule,
                    'plan': plan,
                    'dernier_entretien': entretien,
                    'prochain_km': prochain_km,
                    'km_restants': km_restants,
                    'en_retard': km_restants < 0,
                })

    # Tri : les plus urgents d'abord
    lignes_date.sort(key=lambda l: l['jours_restants'])
    lignes_km.sort(key=lambda l: l['km_restants'] if l['km_restants'] is not None else 999999)

    context = {
        'title': "Plan d'entretien & rappels",
        'lignes_date': lignes_date,
        'lignes_km': lignes_km,
    }
    return render(request, 'maintenance/plan_entretien.html', context)

