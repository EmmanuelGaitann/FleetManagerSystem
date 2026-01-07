import csv
from django.http import HttpResponse

from django.shortcuts import render
from .models import SimulationTrajet
from .forms import SimulationTrajetForm
from decimal import Decimal
from .models import AlerteSysteme
from .services import generer_alertes_echeances
from django.db.models import Sum, F, Q, Max, Min
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from flotte.views import role_required
from flotte.models import Vehicule
from carburant.models import Ravitaillement
from maintenance.models import (
    Entretien,
    Assurance,
    TaxeCirculation,
    VisiteTechnique,
    Anomalie,
)


# ==========================================================
# 1. RAPPORT TCO (Coût Total de Possession)
# ==========================================================

@role_required('Gestionnaire Flotte')
def rapports_tco(request):
    """
    Rapport de Coûts par Véhicule (TCO)
    - Total carburant
    - Total maintenance
    - Kilométrage estimé
    - Coût / km
    - Coût total (TCO)
    """

    # -------------------------------
    # 1) Coûts carburant par véhicule
    # -------------------------------
    carburant_agg = (
        Ravitaillement.objects
        .values('vehicule_id',
                'vehicule__matricule',
                'vehicule__marque',
                'vehicule__modele')
        .annotate(
            cout_carburant=Sum(F('quantite_litres') * F('prix_unitaire')),
            km_min=Min('kilometrage'),
            km_max=Max('kilometrage'),
        )
    )

    tco_data = {}

    for row in carburant_agg:
        veh_id = row['vehicule_id']
        km_min = row['km_min']
        km_max = row['km_max']

        km_total = 0
        if km_min is not None and km_max is not None and km_max > km_min:
            km_total = km_max - km_min

        tco_data[veh_id] = {
            'vehicule__matricule': row['vehicule__matricule'],
            'vehicule__marque': row['vehicule__marque'],
            'vehicule__modele': row['vehicule__modele'],
            'cout_carburant': row['cout_carburant'] or 0,
            'cout_maintenance': 0,
            'km_total': km_total,
        }

    # --------------------------------
    # 2) Coûts maintenance par véhicule
    # --------------------------------
    maintenance_agg = (
        Entretien.objects
        .values('vehicule_id',
                'vehicule__matricule',
                'vehicule__marque',
                'vehicule__modele')
        .annotate(
            cout_maintenance=Sum('cout_total')
        )
    )

    for row in maintenance_agg:
        veh_id = row['vehicule_id']
        cout_maintenance = row['cout_maintenance'] or 0

        if veh_id in tco_data:
            tco_data[veh_id]['cout_maintenance'] = cout_maintenance
        else:
            # Véhicule qui n'a que de la maintenance et pas (encore) de carburant
            tco_data[veh_id] = {
                'vehicule__matricule': row['vehicule__matricule'],
                'vehicule__marque': row['vehicule__marque'],
                'vehicule__modele': row['vehicule__modele'],
                'cout_carburant': 0,
                'cout_maintenance': cout_maintenance,
                'km_total': 0,
            }

    # --------------------------------
    # 3) Calcul du TCO et du coût / km
    # --------------------------------
    lignes = []

    for veh_id, data in tco_data.items():
        cout_carburant = data['cout_carburant'] or 0
        cout_maintenance = data['cout_maintenance'] or 0
        km_total = data['km_total'] or 0

        tco_total = cout_carburant + cout_maintenance

        if km_total > 0:
            cout_par_km = tco_total / km_total
        else:
            cout_par_km = None

        lignes.append({
            'vehicule__matricule': data['vehicule__matricule'],
            'vehicule__marque': data['vehicule__marque'],
            'vehicule__modele': data['vehicule__modele'],
            'cout_carburant': cout_carburant,
            'cout_maintenance': cout_maintenance,
            'km_total': km_total,
            'cout_par_km': cout_par_km,
            'tco_total': tco_total,
        })

    # Tri par matricule pour un affichage propre
    lignes = sorted(lignes, key=lambda x: x['vehicule__matricule'])

    context = {
        'title': 'Rapport de Coûts par Véhicule',
        'lignes': lignes,
    }
    return render(request, 'rapports/rapports_tco.html', context)


# ==========================================================
# 2. RAPPORT PERFORMANCE (Consommation)
# ==========================================================

@role_required('Gestionnaire Flotte')
def rapports_performance(request):
    # 1. Calculer le kilométrage total et les litres consommés par véhicule
    performance_data = Ravitaillement.objects.values('vehicule__matricule', 'vehicule__marque', 'vehicule__modele').annotate(
        litres_total=Sum('quantite_litres'),
        # Pour le kilométrage, nous ne pouvons pas simplement sommer.
        # Nous prenons le max - min. Cela suppose que le premier ravitaillement a le km initial.
        # Pour simplifier ici, nous allons simplement afficher le kilométrage maximum enregistré.
        kilometrage_max=F('kilometrage'), # On récupère le dernier km enregistré (pour chaque ligne)
    ).order_by('vehicule__matricule', '-date_plein')

    # Utilisation d'un dictionnaire pour s'assurer que nous n'avons qu'une seule entrée par véhicule
    # et pour pouvoir calculer la consommation moyenne si le max et min sont disponibles.
    final_performance_rapport = {}

    for item in performance_data:
        matricule = item['vehicule__matricule']
        if matricule not in final_performance_rapport:
            # Récupérer le kilométrage minimum (le plus ancien) du véhicule (Première ligne de ravitaillement)
            # Cette méthode est plus précise: on prend le dernier km enregistré par le système.
            kilometrage_initial = item['vehicule__matricule'].split('-')[0] # Hypotéique: Si le matricule donne l'info

            # Pour la démo, prenons le MIN et MAX pour avoir le total parcouru.
            kilometrage_min = Ravitaillement.objects.filter(vehicule__matricule=matricule).order_by('kilometrage').first().kilometrage if Ravitaillement.objects.filter(vehicule__matricule=matricule).exists() else 0
            kilometrage_max = Ravitaillement.objects.filter(vehicule__matricule=matricule).order_by('-kilometrage').first().kilometrage if Ravitaillement.objects.filter(vehicule__matricule=matricule).exists() else 0

            kilometrage_total_parcouru = kilometrage_max - kilometrage_min

            litres = item['litres_total']

            # Calcul de la consommation moyenne (L/100Km)
            if kilometrage_total_parcouru and litres:
                consommation_moyenne = (litres / kilometrage_total_parcouru) * 100
            else:
                consommation_moyenne = None

            # On agrège toutes les données de ravitaillement (Somme des litres)
            sum_litres = Ravitaillement.objects.filter(vehicule__matricule=matricule).aggregate(total=Sum('quantite_litres'))['total'] or 0

            final_performance_rapport[matricule] = {
                'vehicule__matricule': matricule,
                'vehicule__marque': item['vehicule__marque'],
                'vehicule__modele': item['vehicule__modele'],
                'kilometrage_total': kilometrage_total_parcouru,
                'litres_total': sum_litres,
                'consommation_moyenne': consommation_moyenne
            }

    context = {
        'performance_rapport': final_performance_rapport.values(),
        'title': 'Rapport de Performance',
    }
    return render(request, 'rapports/rapports_performance.html', context)


# ==========================================================
# 3. LISTE DES ALERTES (Rappels d'échéances)
# ==========================================================

@role_required('Gestionnaire Flotte')
def alerte_list(request):
    aujourdhui = timezone.now().date()
    limite_jours = 30 # Alertes pour les 30 prochains jours (ou déjà expirées)
    date_limite = aujourdhui + timedelta(days=limite_jours)

    alertes = []

    # --- 1. Alertes Assurance ---
    # On filtre les assurances dont la date d'expiration est avant la date limite
    assurances_urgentes = Assurance.objects.filter(
        expiration_assurance__lte=date_limite,
    ).select_related('vehicule').order_by('expiration_assurance')

    for ass in assurances_urgentes:
        # Calculer les jours restants (nombre entier)
        jours_restants = (ass.expiration_assurance - aujourdhui).days
        alertes.append({
            'vehicule__matricule': ass.vehicule.matricule,
            'type_alerte': 'Assurance',
            'expiration': ass.expiration_assurance,
            'rappel_avant_jours': ass.rappel_avant_jours,
            'jours_restants': jours_restants,
        })

    # --- 2. Alertes Taxes de Circulation ---
    taxes_urgentes = TaxeCirculation.objects.filter(
        expiration__lte=date_limite,
    ).select_related('vehicule').order_by('expiration')

    for taxe in taxes_urgentes:
        jours_restants = (taxe.expiration - aujourdhui).days
        alertes.append({
            'vehicule__matricule': taxe.vehicule.matricule,
            'type_alerte': 'Taxe Circulation',
            'expiration': taxe.expiration,
            'rappel_avant_jours': taxe.rappel_avant_jours,
            'jours_restants': jours_restants,
        })

    # --- 3. Alertes Visites Techniques ---
    visites_urgentes = VisiteTechnique.objects.filter(
        prochaine_visite__lte=date_limite,
    ).select_related('vehicule').order_by('prochaine_visite')

    for visite in visites_urgentes:
        jours_restants = (visite.prochaine_visite - aujourdhui).days
        alertes.append({
            'vehicule__matricule': visite.vehicule.matricule,
            'type_alerte': 'Visite Technique',
            'expiration': visite.prochaine_visite,
            'rappel_avant_jours': visite.rappel_avant_jours,
            'jours_restants': jours_restants,
        })

    # Trier les alertes par jours_restants (les plus urgentes en premier)
    alertes_triees = sorted(alertes, key=lambda x: x['jours_restants'])

    context = {
        'alertes': alertes_triees,
        'title': 'Liste des Alertes et Rappels',
    }
    return render(request, 'rapports/alerte_list.html', context)
# ==========================================================
#  MODULE : SIMULATION DE TRAJET
# ==========================================================

@role_required('Gestionnaire Flotte')
def simulation_trajet(request):
    """
    Vue de simulation de trajet (Module 5 du CDC).

    Pour rester simple (sans clé API obligatoire) :
    - L'utilisateur saisit point A, B, distance, durée, conso moyenne, prix du carburant.
    - Le système calcule le coût estimé et sauvegarde la simulation.
    - On affiche aussi l'historique des dernières simulations.
    """
    if request.method == 'POST':
        form = SimulationTrajetForm(request.POST)
        if form.is_valid():
            simulation: SimulationTrajet = form.save(commit=False)
            simulation.utilisateur = request.user

            prix_carburant_litre = form.cleaned_data['prix_carburant_litre']
            distance_km = simulation.distance_km
            conso_l_100 = simulation.consommation_moyenne_l_100

            # Algorithme simple : litres = distance * conso / 100
            litres_estimes = (distance_km * conso_l_100) / Decimal('100')
            cout_estime = litres_estimes * prix_carburant_litre

            simulation.cout_estime_carburant = cout_estime
            simulation.save()

            # On prépare un formulaire vide pour une nouvelle simulation
            form = SimulationTrajetForm()
            message_succes = "Simulation enregistrée avec succès."

            simulations = SimulationTrajet.objects.all()[:10]

            context = {
                'form': form,
                'simulations': simulations,
                'derniere_simulation': simulation,
                'message_succes': message_succes,
                'title': 'Simulation de Trajet',
            }
            return render(request, 'rapports/simulation_trajet.html', context)
    else:
        form = SimulationTrajetForm()

    simulations = SimulationTrajet.objects.all()[:10]

    context = {
        'form': form,
        'simulations': simulations,
        'title': 'Simulation de Trajet',
    }
    return render(request, 'rapports/simulation_trajet.html', context)

@role_required("Gestionnaire Flotte")
def alertes_echeances(request):
    generer_alertes_echeances()  # refresh auto quand on ouvre la page

    alertes = AlerteSysteme.objects.filter(est_resolue=False).order_by("date_echeance")

    return render(request, "rapports/alertes_echeances.html", {
        "alertes": alertes,
        "title": "Alertes d’échéances",
    })

# ==========================================================
# RAPPORT D'UTILISATION (Kilométrage par mois)
# ==========================================================

@role_required('Gestionnaire Flotte')
def rapports_utilisation(request):
    """
    Rapport d'utilisation :
    - Affiche, par véhicule et par mois, le kilométrage parcouru.
    - Basé sur les relevés de carburant (Ravitaillement.kilometrage).
    """
    # 1) On prend tous les ravitaillements, groupés par véhicule + mois
    ravitaillements = (
        Ravitaillement.objects
        .annotate(mois=TruncMonth('date_plein'))
        .values('vehicule__matricule', 'vehicule__marque', 'vehicule__modele', 'mois')
        .annotate(
            km_min=Min('kilometrage'),
            km_max=Max('kilometrage'),
        )
        .order_by('vehicule__matricule', 'mois')
    )

    utilisation_data = []

    for item in ravitaillements:
        km_min = item['km_min'] or 0
        km_max = item['km_max'] or 0
        km_parcourus = km_max - km_min if km_max and km_min else 0

        utilisation_data.append({
            'vehicule__matricule': item['vehicule__matricule'],
            'vehicule__marque': item['vehicule__marque'],
            'vehicule__modele': item['vehicule__modele'],
            'mois': item['mois'],
            'km_min': km_min,
            'km_max': km_max,
            'km_parcourus': km_parcourus,
        })

    context = {
        'utilisation_data': utilisation_data,
        'title': 'Rapport d’utilisation',
    }
    return render(request, 'rapports/rapports_utilisation.html', context)


@role_required('Gestionnaire Flotte')
def export_utilisation_csv(request):
    """
    Exporte le rapport d'utilisation (km/mois par véhicule) au format CSV.
    Ouvrable directement avec Excel.
    """
    # Même logique que dans rapports_utilisation
    ravitaillements = (
        Ravitaillement.objects
        .annotate(mois=TruncMonth('date_plein'))
        .values('vehicule__matricule', 'vehicule__marque', 'vehicule__modele', 'mois')
        .annotate(
            km_min=Min('kilometrage'),
            km_max=Max('kilometrage'),
        )
        .order_by('vehicule__matricule', 'mois')
    )

    utilisation_data = []

    for item in ravitaillements:
        km_min = item['km_min'] or 0
        km_max = item['km_max'] or 0
        km_parcourus = km_max - km_min if km_max and km_min else 0

        utilisation_data.append({
            'vehicule__matricule': item['vehicule__matricule'],
            'vehicule__marque': item['vehicule__marque'],
            'vehicule__modele': item['vehicule__modele'],
            'mois': item['mois'],
            'km_min': km_min,
            'km_max': km_max,
            'km_parcourus': km_parcourus,
        })

    # Préparation de la réponse CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rapport_utilisation.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Matricule',
        'Marque',
        'Modèle',
        'Mois',
        'Km min',
        'Km max',
        'Km parcourus',
    ])

    for item in utilisation_data:
        writer.writerow([
            item['vehicule__matricule'],
            item['vehicule__marque'],
            item['vehicule__modele'],
            item['mois'].strftime('%m/%Y') if item['mois'] else '',
            item['km_min'],
            item['km_max'],
            item['km_parcourus'],
        ])

    return response

# ==========================================================
# RAPPORT D'ANOMALIES
# ==========================================================

@role_required('Gestionnaire Flotte')
def rapports_anomalies(request):
    """
    Rapport d'anomalies :
    - Liste toutes les anomalies déclarées.
    - Permet de filtrer rapidement visuellement par véhicule, type, statut.
    """
    anomalies = (
        Anomalie.objects
        .select_related('vehicule', 'conducteur')
        .order_by('-date_declaration')
    )

    context = {
        'anomalies': anomalies,
        'title': 'Rapport d’anomalies',
    }
    return render(request, 'rapports/rapports_anomalies.html', context)

@role_required('Gestionnaire Flotte')
def export_anomalies_csv(request):
    """
    Exporte le rapport d'anomalies au format CSV.
    """
    anomalies = (
        Anomalie.objects
        .select_related('vehicule', 'conducteur')
        .order_by('-date_declaration')
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rapport_anomalies.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Véhicule',
        'Conducteur',
        'Type anomalie',
        'Statut',
        'Date déclaration',
        'Description',
    ])

    for a in anomalies:
        conducteur_nom = ""
        if a.conducteur:
            nom = getattr(a.conducteur, 'nom', '') or ''
            prenom = getattr(a.conducteur, 'prenom', '') or ''
            conducteur_nom = f"{nom} {prenom}".strip()

        writer.writerow([
            getattr(a.vehicule, 'matricule', '') if a.vehicule else '',
            conducteur_nom,
            getattr(a, 'type_anomalie', ''),
            getattr(a, 'statut', ''),
            a.date_declaration.strftime('%d/%m/%Y %H:%M') if a.date_declaration else '',
            (a.description or '').replace('\n', ' ').strip(),
        ])

    return response

@role_required('Gestionnaire Flotte')
def rapports_anomalies(request):
    """
    Rapport d'Anomalies :
    - Surconsommation carburant (calcul entre deux pleins)
    - Incidents déclarés (table Anomalie)
    """

    # -----------------------------
    # 1) Détection surconsommation
    # -----------------------------

    # Seuils simples par type de carburant (tu pourras ajuster facilement)
    SEUILS_CONSO = {
        'diesel': 10.0,   # L/100 km
        'gasoil': 10.0,
        'essence': 13.0,
        'super': 13.0,
        'default': 12.0,
    }

    surconsommations = []

    # On récupère tous les pleins, groupés par véhicule puis triés par date + kilométrage
    ravitaillements = (
        Ravitaillement.objects
        .select_related('vehicule')
        .order_by('vehicule_id', 'date_plein', 'kilometrage')
    )

    current_veh_id = None
    prev_rav = None

    for r in ravitaillements:
        if r.kilometrage is None or r.quantite_litres is None:
            # Si on n'a pas de km ou de litres, on ne peut pas calculer
            continue

        if current_veh_id != r.vehicule_id:
            # Nouveau véhicule, on remet à zéro la séquence
            current_veh_id = r.vehicule_id
            prev_rav = r
            continue

        # Même véhicule, on peut comparer avec le plein précédent
        distance = r.kilometrage - (prev_rav.kilometrage or 0)

        if distance > 0 and r.quantite_litres > 0:
            # Consommation (L/100 km) entre prev_rav et r
            conso_l_100 = float(r.quantite_litres) / float(distance) * 100.0

            type_carb = (r.vehicule.type_carburant or '').lower()
            seuil = SEUILS_CONSO.get(type_carb, SEUILS_CONSO['default'])

            if conso_l_100 > seuil:
                surconsommations.append({
                    'vehicule': r.vehicule,
                    'date_debut': prev_rav.date_plein,
                    'date_fin': r.date_plein,
                    'km_debut': prev_rav.kilometrage,
                    'km_fin': r.kilometrage,
                    'distance': distance,
                    'litres': float(r.quantite_litres),
                    'conso_calculee': conso_l_100,
                    'seuil': seuil,
                })

        # On avance le pointeur
        prev_rav = r

    # On trie les surconsommations les plus récentes en premier
    surconsommations = sorted(
        surconsommations,
        key=lambda x: (x['vehicule'].matricule, x['date_fin'] or x['date_debut']),
        reverse=True
    )

    # -----------------------------
    # 2) Incidents/anomalies déclarés
    # -----------------------------
    incidents = (
        Anomalie.objects
        .select_related('vehicule', 'conducteur')
        .order_by('-date_declaration')
    )

    context = {
        'title': "Rapport d'Anomalies",
        'surconsommations': surconsommations,
        'incidents': incidents,
    }
    return render(request, 'rapports/rapports_anomalies.html', context)
