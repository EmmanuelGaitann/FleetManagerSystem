# carburant/models.py (MODIFICATION IMPORTANTE)

from django.db import models
from flotte.models import Vehicule
from fournisseurs.models import Fournisseur

class Ravitaillement(models.Model):
    vehicule = models.ForeignKey(Vehicule, models.PROTECT)
    fournisseur = models.ForeignKey(Fournisseur, models.SET_NULL, blank=True, null=True)

    date_plein = models.DateTimeField(db_comment='Date et heure du ravitaillement')
    kilometrage = models.IntegerField(db_comment='Kilométrage au moment du plein')
    quantite_litres = models.DecimalField(max_digits=8, decimal_places=2, db_column='quantite', db_comment='Quantité en Litres')
    prix_unitaire = models.DecimalField(max_digits=8, decimal_places=2, db_comment='Prix du litre')
    # total_depense est supprimé car il n'existe pas en BDD

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Plein pour {self.vehicule.matricule} le {self.date_plein.strftime('%d/%m/%Y')}"

    class Meta:
        managed = False
        db_table = 'carburants'  # Nom de table confirmé
        verbose_name = "Ravitaillement"
        verbose_name_plural = "Ravitaillements"