from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Q, F
import datetime
from django.urls import reverse_lazy

# IMPORTS DES MODÈLES (Assumant qu'ils sont définis dans flotte/models.py)
# J'ai retiré Ravitaillement car le modèle n'est pas fourni dans les imports.
from .models import Departement, Vehicule, Conducteur, Affectation, Assurance, TaxeCirculation, VisiteTechnique
# Imports des Formulaires (Assumant qu'ils sont définis dans flotte/forms.py)
from .forms import DepartementForm, VehiculeForm, ConducteurForm, AffectationForm

from django.utils import timezone
from carburant.models import Ravitaillement
from maintenance.models import Entretien, Anomalie

try:
    from rapports.models import AlerteSysteme
except Exception:
    AlerteSysteme = None

# -----------------------------------------------------------
# Décorateur RBAC (Contrôle d'Accès basé sur les Rôles)
# -----------------------------------------------------------

def role_required(*allowed_roles):
    """
    Décorateur personnalisé pour limiter l'accès à une vue à un ou plusieurs rôles.
    Exemple d'usage :
        @role_required('Gestionnaire Flotte')
        @role_required('Gestionnaire Flotte', 'Administrateur Système')
    Le superuser a toujours accès.
    """
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            # 1. Le superuser a toujours accès
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # 2. Récupération du nom de rôle de l'utilisateur (peut être None)
            user_role_obj = getattr(request.user, 'role', None)
            user_role_name = getattr(user_role_obj, 'nom', None)

            # 3. Si le rôle de l'utilisateur fait partie des rôles autorisés → OK
            if user_role_name in allowed_roles:
                return view_func(request, *args, **kwargs)

            # 4. Sinon, on le renvoie gentiment au dashboard
            return redirect('dashboard')

        return wrapper
    return decorator



# -----------------------------------------------------------
# Vues Générales
# -----------------------------------------------------------
@login_required
def dashboard_view(request):
    """Affiche le tableau de bord principal après connexion avec les KPI FMS."""

    # Rôle utilisateur (affiché dans le badge vert)
    user_role_name = (
        request.user.role.nom
        if hasattr(request.user, "role") and getattr(request.user, "role", None)
        else "Invité"
    )

    # Date du jour et début du mois courant
    today = timezone.now().date()
    first_day_month = today.replace(day=1)

    # 1) KPI de base
    total_vehicules = Vehicule.objects.count()
    total_conducteurs = Conducteur.objects.count()

    # 2) Affectations en cours (date_fin vide ou dans le futur)
    affectations_qs = Affectation.objects.filter(
        Q(date_fin__isnull=True) | Q(date_fin__gte=today)
    )

    affectations_en_cours = affectations_qs.count()

    # Dernière affectation en cours (pour le bloc "Affectation actuelle")
    affectation_actuelle = (
        affectations_qs.select_related("vehicule", "conducteur")
        .order_by("-date_debut")
        .first()
    )

    # 3) Alertes urgentes (non résolues)
    alertes_urgentes = 0
    if AlerteSysteme is not None:
        try:
            alertes_urgentes = (
                AlerteSysteme.objects.filter(est_resolue=False).count()
            )
        except Exception:
            alertes_urgentes = 0

    # (Tu pourras plus tard ajouter ici :
    #  - total carburant du mois,
    #  - coût maintenance du mois, etc.)

    context = {
        "user_role": user_role_name,
        "title": "Tableau de Bord FMS",

        # KPI utilisés dans dashboard.html
        "total_vehicules": total_vehicules,
        "total_conducteurs": total_conducteurs,
        "affectations_en_cours": affectations_en_cours,
        "affectation_actuelle": affectation_actuelle,
        "alertes": {
            "total_urgentes": alertes_urgentes,
        },
    }

    return render(request, "dashboard.html", context)



# -----------------------------------------------------------
# Vues CRUD du Module Départements (Fonctions basées sur votre code)
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def departement_list(request):
    departements = Departement.objects.all().order_by('nom')
    context = {'departements': departements, 'title': 'Liste des Départements'}
    return render(request, 'flotte/departement_list.html', context)

@role_required('Gestionnaire Flotte')
def departement_create(request):
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departement_list')
    else:
        form = DepartementForm()
    context = {'form': form, 'title': 'Ajouter un Département', 'action': 'Créer'}
    return render(request, 'flotte/departement_form.html', context)

@role_required('Gestionnaire Flotte')
def departement_update(request, pk):
    departement = get_object_or_404(Departement, pk=pk)
    if request.method == 'POST':
        form = DepartementForm(request.POST, instance=departement)
        if form.is_valid():
            form.save()
            return redirect('departement_list')
    else:
        form = DepartementForm(instance=departement)
    context = {'form': form, 'title': 'Modifier le Département', 'action': 'Sauvegarder'}
    return render(request, 'flotte/departement_form.html', context)

@role_required('Gestionnaire Flotte')
def departement_delete(request, pk):
    departement = get_object_or_404(Departement, pk=pk)
    if request.method == 'POST':
        departement.delete()
        return redirect('departement_list')
    context = {'departement': departement, 'title': 'Supprimer le Département'}
    return render(request, 'flotte/departement_confirm_delete.html', context)


# -----------------------------------------------------------
# Vues CRUD du Module Véhicules
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def vehicule_list(request):
    vehicules = Vehicule.objects.select_related('departement').all()
    return render(request, 'flotte/vehicule_list.html', {'vehicules': vehicules, 'title': 'Liste des Véhicules'})

@role_required('Gestionnaire Flotte')
def vehicule_create(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicule_list')
    else:
        form = VehiculeForm()
    return render(request, 'flotte/vehicule_form.html', {'form': form, 'title': 'Ajouter un Véhicule', 'action': 'Créer'})

@role_required('Gestionnaire Flotte')
def vehicule_update(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            return redirect('vehicule_list')
    else:
        form = VehiculeForm(instance=vehicule)
    return render(request, 'flotte/vehicule_form.html', {'form': form, 'title': 'Modifier le Véhicule', 'action': 'Sauvegarder'})

@role_required('Gestionnaire Flotte')
def vehicule_delete(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        vehicule.delete()
        return redirect('vehicule_list')
    return render(request, 'flotte/vehicule_confirm_delete.html', {'vehicule': vehicule, 'title': 'Supprimer le Véhicule'})

# -----------------------------------------------------------
# Vues CRUD du Module Conducteurs
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def conducteur_list(request):
    conducteurs = Conducteur.objects.all().order_by('nom', 'prenom')
    return render(request, 'flotte/conducteur_list.html', {'conducteurs': conducteurs, 'title': 'Liste des Conducteurs'})

@role_required('Gestionnaire Flotte')
def conducteur_create(request):
    if request.method == 'POST':
        form = ConducteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('conducteur_list')
    else:
        form = ConducteurForm()
    return render(request, 'flotte/conducteur_form.html', {'form': form, 'title': 'Ajouter un Conducteur', 'action': 'Créer'})

@role_required('Gestionnaire Flotte')
def conducteur_update(request, pk):
    conducteur = get_object_or_404(Conducteur, pk=pk)
    if request.method == 'POST':
        form = ConducteurForm(request.POST, instance=conducteur)
        if form.is_valid():
            form.save()
            return redirect('conducteur_list')
    else:
        form = ConducteurForm(instance=conducteur)
    return render(request, 'flotte/conducteur_form.html', {'form': form, 'title': 'Modifier le Conducteur', 'action': 'Sauvegarder'})

@role_required('Gestionnaire Flotte')
def conducteur_delete(request, pk):
    conducteur = get_object_or_404(Conducteur, pk=pk)
    if request.method == 'POST':
        conducteur.delete()
        return redirect('conducteur_list')
    return render(request, 'flotte/conducteur_confirm_delete.html', {'conducteur': conducteur, 'title': 'Supprimer le Conducteur'})


# -----------------------------------------------------------
# Vues CRUD du Module Affectations
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def affectation_list(request):
    affectations = Affectation.objects.select_related('vehicule', 'conducteur').order_by('-date_debut')
    return render(request, 'flotte/affectation_list.html', {'affectations': affectations, 'title': 'Gestion des Affectations'})

@role_required('Gestionnaire Flotte')
def affectation_create(request):
    if request.method == 'POST':
        form = AffectationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affectation_list')
    else:
        form = AffectationForm()
    return render(request, 'flotte/affectation_form.html', {'form': form, 'title': 'Créer une Affectation', 'action': 'Créer'})

@role_required('Gestionnaire Flotte')
def affectation_update(request, pk):
    affectation = get_object_or_404(Affectation, pk=pk)
    if request.method == 'POST':
        form = AffectationForm(request.POST, instance=affectation)
        if form.is_valid():
            form.save()
            return redirect('affectation_list')
    else:
        form = AffectationForm(instance=affectation)
    return render(request, 'flotte/affectation_form.html', {'form': form, 'title': 'Modifier l\'Affectation', 'action': 'Sauvegarder'})

@role_required('Gestionnaire Flotte')
def affectation_delete(request, pk):
    affectation = get_object_or_404(Affectation, pk=pk)
    if request.method == 'POST':
        affectation.delete()
        return redirect('affectation_list')
    return render(request, 'flotte/affectation_confirm_delete.html', {'affectation': affectation, 'title': 'Supprimer l\'Affectation'})


# -----------------------------------------------------------
# Vues du Tableau de Bord & Alertes
# -----------------------------------------------------------

@role_required('Gestionnaire Flotte')
def alerte_list(request):
    aujourdhui = datetime.date.today()

    # Alertes Assurances
    assurances_a_alerter = Assurance.objects.select_related('vehicule').filter(
        Q(expiration_assurance__gte=aujourdhui) &
        Q(expiration_assurance__lte=aujourdhui + F('rappel_avant_jours') * datetime.timedelta(days=1))
    ).order_by('expiration_assurance')

    # Alertes Taxes de Circulation
    taxes_a_alerter = TaxeCirculation.objects.select_related('vehicule').filter(
        Q(expiration__gte=aujourdhui) &
        Q(expiration__lte=aujourdhui + F('rappel_avant_jours') * datetime.timedelta(days=1))
    ).order_by('expiration')

    # Alertes Visites Techniques
    visites_a_alerter = VisiteTechnique.objects.select_related('vehicule').filter(
        Q(prochaine_visite__gte=aujourdhui) &
        Q(prochaine_visite__lte=aujourdhui + F('rappel_avant_jours') * datetime.timedelta(days=1))
    ).order_by('prochaine_visite')

    alertes = {
        'assurances': assurances_a_alerter,
        'taxes': taxes_a_alerter,
        'visites': visites_a_alerter,
    }

    return render(request, 'flotte/alerte_list.html', {'alertes': alertes, 'title': 'Tableau de Bord des Alertes'})


# ==========================================================
# Vues CRUD Rappels (Utilisation des classes génériques)
# ==========================================================

class AssuranceListView(generic.ListView):
    model = Assurance
    template_name = 'flotte/assurance_list.html'
    context_object_name = 'assurances'
assurance_list = role_required('Gestionnaire Flotte')(AssuranceListView.as_view())

class AssuranceCreateView(generic.CreateView):
    model = Assurance
    fields = ['vehicule', 'date_assurance', 'expiration_assurance', 'rappel_avant_jours', 'note']
    template_name = 'flotte/assurance_form.html'
    success_url = reverse_lazy('assurance_list')
assurance_create = role_required('Gestionnaire Flotte')(AssuranceCreateView.as_view())

class AssuranceUpdateView(generic.UpdateView):
    model = Assurance
    fields = ['vehicule', 'date_assurance', 'expiration_assurance', 'rappel_avant_jours', 'note']
    template_name = 'flotte/assurance_form.html'
    success_url = reverse_lazy('assurance_list')
assurance_update = role_required('Gestionnaire Flotte')(AssuranceUpdateView.as_view())

class AssuranceDeleteView(generic.DeleteView):
    model = Assurance
    template_name = 'flotte/assurance_confirm_delete.html'
    success_url = reverse_lazy('assurance_list')
assurance_delete = role_required('Gestionnaire Flotte')(AssuranceDeleteView.as_view())


class TaxeCirculationListView(generic.ListView):
    model = TaxeCirculation
    template_name = 'flotte/taxe_list.html'
    context_object_name = 'taxes'
taxe_list = role_required('Gestionnaire Flotte')(TaxeCirculationListView.as_view())

class TaxeCirculationCreateView(generic.CreateView):
    model = TaxeCirculation
    fields = ['vehicule', 'date_taxe_circulation', 'expiration', 'rappel_avant_jours', 'note']
    template_name = 'flotte/taxe_form.html'
    success_url = reverse_lazy('taxe_list')
taxe_create = role_required('Gestionnaire Flotte')(TaxeCirculationCreateView.as_view())

class TaxeCirculationUpdateView(generic.UpdateView):
    model = TaxeCirculation
    fields = ['vehicule', 'date_taxe_circulation', 'expiration', 'rappel_avant_jours', 'note']
    template_name = 'flotte/taxe_form.html'
    success_url = reverse_lazy('taxe_list')
taxe_update = role_required('Gestionnaire Flotte')(TaxeCirculationUpdateView.as_view())

class TaxeCirculationDeleteView(generic.DeleteView):
    model = TaxeCirculation
    template_name = 'flotte/taxe_confirm_delete.html'
    success_url = reverse_lazy('taxe_list')
taxe_delete = role_required('Gestionnaire Flotte')(TaxeCirculationDeleteView.as_view())


class VisiteTechniqueListView(generic.ListView):
    model = VisiteTechnique
    template_name = 'flotte/visite_list.html'
    context_object_name = 'visites'
visite_list = role_required('Gestionnaire Flotte')(VisiteTechniqueListView.as_view())

class VisiteTechniqueCreateView(generic.CreateView):
    model = VisiteTechnique
    fields = ['vehicule', 'derniere_visite', 'prochaine_visite', 'rappel_avant_jours', 'note']
    template_name = 'flotte/visite_form.html'
    success_url = reverse_lazy('visite_list')
visite_create = role_required('Gestionnaire Flotte')(VisiteTechniqueCreateView.as_view())

class VisiteTechniqueUpdateView(generic.UpdateView):
    model = VisiteTechnique
    fields = ['vehicule', 'derniere_visite', 'prochaine_visite', 'rappel_avant_jours', 'note']
    template_name = 'flotte/visite_form.html'
    success_url = reverse_lazy('visite_list')
visite_update = role_required('Gestionnaire Flotte')(VisiteTechniqueUpdateView.as_view())

class VisiteTechniqueDeleteView(generic.DeleteView):
    model = VisiteTechnique
    template_name = 'flotte/visite_confirm_delete.html'
    success_url = reverse_lazy('visite_list')
visite_delete = role_required('Gestionnaire Flotte')(VisiteTechniqueDeleteView.as_view())


@login_required
def mes_affectations(request):
    """
    Espace chauffeur :
    - Affiche le véhicule actuellement affecté au chauffeur connecté
    - Affiche l'historique de ses affectations
    """

    # On suppose que "conducteur" == personne portant le même nom/prénom/email que le compte
    utilisateur = request.user

    # Il faut retrouver le conducteur lié à ce compte
    from flotte.models import Conducteur, Affectation

    conducteur = Conducteur.objects.filter(
        email=utilisateur.email
    ).first()

    if not conducteur:
        # Cas rare : compte sans fiche conducteur associée
        return render(request, "flotte/mes_affectations.html", {
            "pas_de_conducteur": True
        })

    today = timezone.now().date()

    # Affectation en cours
    affectation_actuelle = Affectation.objects.filter(
        conducteur=conducteur,
        date_debut__lte=today,
        # pas de date de fin OU fin future
        # (donc l'affectation est encore active)
        # ================================
        date_fin__isnull=True
    ).order_by("-date_debut").first()

    if not affectation_actuelle:
        affectation_actuelle = Affectation.objects.filter(
            conducteur=conducteur,
            date_debut__lte=today,
            date_fin__gte=today
        ).order_by("-date_debut").first()

    # Historique complet
    historique = Affectation.objects.filter(
        conducteur=conducteur
    ).order_by("-date_debut")

    context = {
        "conducteur": conducteur,
        "affectation_actuelle": affectation_actuelle,
        "historique": historique,
    }
    return render(request, "flotte/mes_affectations.html", context)