# rapports/services.py

from datetime import date, timedelta

from flotte.models import Assurance, TaxeCirculation, VisiteTechnique
from .models import AlerteSysteme


def _creer_alerte_si_absente(vehicule, type_alerte, date_echeance, message):
    """
    Crée une alerte si elle n'existe pas déjà pour ce véhicule, ce type et cette date.
    """
    if not date_echeance:
        return

    AlerteSysteme.objects.get_or_create(
        vehicule=vehicule,
        type_alerte=type_alerte,
        date_echeance=date_echeance,
        est_resolue=False,
        defaults={
            "message": message,
        },
    )


def generer_alertes_echeances():
    """
    Génère les alertes à partir des tables :
    - Assurance
    - TaxeCirculation
    - VisiteTechnique

    Utilise le champ `rappel_avant_jours` de chaque enregistrement pour savoir
    quand commencer à alerter.
    """
    aujourd_hui = date.today()

    # =========================
    # 1) ASSURANCES
    # =========================
    assurances = Assurance.objects.all()

    for a in assurances:
        if not a.expiration_assurance:
            continue

        # nombre de jours avant expiration pour lancer l'alerte
        rappel = a.rappel_avant_jours or 0
        date_debut_alerte = a.expiration_assurance - timedelta(days=rappel)

        # On alerte si on est entre la date de début d'alerte et la date d'expiration
        if date_debut_alerte <= aujourd_hui <= a.expiration_assurance:
            _creer_alerte_si_absente(
                vehicule=a.vehicule,
                type_alerte="assurance",
                date_echeance=a.expiration_assurance,
                message="Assurance proche de l'échéance",
            )

    # =========================
    # 2) TAXES DE CIRCULATION
    # =========================
    taxes = TaxeCirculation.objects.all()

    for t in taxes:
        if not t.expiration:
            continue

        rappel = t.rappel_avant_jours or 0
        date_debut_alerte = t.expiration - timedelta(days=rappel)

        if date_debut_alerte <= aujourd_hui <= t.expiration:
            _creer_alerte_si_absente(
                vehicule=t.vehicule,
                type_alerte="taxe",
                date_echeance=t.expiration,
                message="Taxe de circulation bientôt expirée",
            )

    # =========================
    # 3) VISITES TECHNIQUES
    # =========================
    visites = VisiteTechnique.objects.all()

    for v in visites:
        if not v.prochaine_visite:
            continue

        rappel = v.rappel_avant_jours or 0
        date_debut_alerte = v.prochaine_visite - timedelta(days=rappel)

        if date_debut_alerte <= aujourd_hui <= v.prochaine_visite:
            _creer_alerte_si_absente(
                vehicule=v.vehicule,
                type_alerte="visite_technique",
                date_echeance=v.prochaine_visite,
                message="Visite technique à planifier",
            )
