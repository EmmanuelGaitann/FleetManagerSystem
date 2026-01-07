from django.db import models
from flotte.models import Vehicule
from utilisateurs.models import User


class SimulationTrajet(models.Model):
    """
    Module 5 : Simulation de Trajet
    Sauvegarde des itinéraires simulés (CDC).
    """
    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Véhicule utilisé pour la simulation (optionnel)."
    )
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Utilisateur ayant lancé la simulation."
    )

    point_depart = models.CharField(max_length=255)
    point_arrivee = models.CharField(max_length=255)

    # Résultats de simulation
    distance_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Distance estimée en kilomètres."
    )
    duree_minutes = models.PositiveIntegerField(
        help_text="Durée estimée en minutes."
    )

    # Estimation consommation / coût
    consommation_moyenne_l_100 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Consommation moyenne (L/100 km) utilisée pour l'estimation.",
        default=8.0
    )
    cout_estime_carburant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Coût estimé du carburant pour ce trajet.",
        null=True,
        blank=True,
    )

    date_simulation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_simulation']
        verbose_name = "Simulation de trajet"
        verbose_name_plural = "Simulations de trajets"

    def __str__(self):
        return f"{self.point_depart} → {self.point_arrivee} ({self.distance_km} km)"

class AlerteSysteme(models.Model):
    TYPE_CHOICES = [
        ("assurance", "Assurance"),
        ("visite_technique", "Visite technique"),
        ("taxe", "Taxe de circulation"),
        ("maintenance", "Maintenance"),
    ]

    vehicule = models.ForeignKey("flotte.Vehicule", on_delete=models.CASCADE)
    type_alerte = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message = models.CharField(max_length=255)

    date_echeance = models.DateField()
    date_generation = models.DateTimeField(auto_now_add=True)

    est_resolue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vehicule} – {self.type_alerte} – {self.date_echeance}"
