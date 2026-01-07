from django.db import models
# Note: Si Fournisseur est dans une application 'fournisseurs', assurez-vous de l'importer correctement
from flotte.models import Vehicule, Conducteur
from fournisseurs.models import Fournisseur

# ====================
# Modèles : Maintenance et Suivi (Carburant, Entretien, Assurances, etc.)
# ====================

class EntretienMaitre(models.Model):
    description = models.CharField(max_length=255)
    repeter_par_date = models.IntegerField(blank=True, null=True, db_comment='Répéter toutes (jours)')
    repeter_par_kilometrage = models.IntegerField(blank=True, null=True, db_comment='Répéter au kilométrage (km)')
    rappel_avant_jours = models.IntegerField(blank=True, null=True, db_comment='Rappel avant (jours)')
    rappel_avant_kilometrage = models.IntegerField(blank=True, null=True, db_comment='Rappel avant (km)')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        managed = False
        db_table = 'entretien_maitres'


class Entretien(models.Model):
    # ON DELETE CASCADE
    vehicule = models.ForeignKey(Vehicule, models.CASCADE)

    # ON DELETE SET NULL
    fournisseur = models.ForeignKey(Fournisseur, models.SET_NULL, blank=True, null=True)
    entretien_maitre = models.ForeignKey(EntretienMaitre, models.SET_NULL, blank=True, null=True, db_comment="Plan d'entretien utilisé")

    description = models.TextField(db_comment="Détail de l'entretien")
    date_entretien = models.DateField(db_comment="Date de l'entretien")
    kilometrage = models.IntegerField(db_comment="Kilométrage au moment de l'entretien")
    note = models.TextField(blank=True, null=True)
    depense_type = models.CharField(max_length=100, blank=True, null=True, db_comment='Ex: Vidange, Réparation')
    cout_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Entretien {self.vehicule} le {self.date_entretien}"

    class Meta:
        managed = False
        db_table = 'entretiens'


class DetailDepense(models.Model):
    # ON DELETE CASCADE
    entretien = models.ForeignKey(Entretien, models.CASCADE)

    description = models.CharField(max_length=255, blank=True, null=True, db_comment="Description de la dépense (Pièce, Main d'oeuvre, etc.)")
    quantite = models.IntegerField()
    cout_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    # ON DELETE SET NULL
    # Assuming 'fournisseurs.Piece' exists. Si Piece est définie dans l'app 'fournisseurs', cela ne devrait pas avoir de conflit avec la Flotte
    piece = models.ForeignKey('fournisseurs.Piece', models.SET_NULL, blank=True, null=True, db_comment="Lien vers une pièce si c'est un remplacement de pièce")

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail_depenses'
        verbose_name_plural = "Détail des Dépenses"


class Carburant(models.Model):
    # ON DELETE CASCADE
    vehicule = models.ForeignKey(Vehicule, models.CASCADE)

    # ON DELETE SET NULL
    fournisseur = models.ForeignKey(Fournisseur, models.SET_NULL, blank=True, null=True)

    date_plein = models.DateTimeField(db_comment='Date, Heure')
    kilometrage = models.IntegerField(db_comment='Kilométrage au moment du plein')
    quantite = models.DecimalField(max_digits=8, decimal_places=2, db_comment='Quantité (Litres)')
    prix_unitaire = models.DecimalField(max_digits=6, decimal_places=3, db_comment='Prix unitaire')
    station_service = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Plein {self.quantite}L pour {self.vehicule}"

    class Meta:
        managed = False
        db_table = 'carburants'


# ==========================================================
# Modèles de Rappels (CORRIGÉ pour related_name)
# ==========================================================

class Assurance(models.Model):
    # CORRECTION : Ajout de related_name pour éviter le conflit avec flotte.Assurance
    vehicule = models.ForeignKey(Vehicule, models.CASCADE, related_name='assurances_maintenance')

    # CORRECTION : Ajout de related_name pour éviter le conflit sur Fournisseur
    fournisseur = models.ForeignKey(
        Fournisseur, models.SET_NULL, blank=True, null=True, db_comment='Assureur',
        related_name='assurances_maintenance'
    )

    date_assurance = models.DateField()
    expiration_assurance = models.DateField()
    rappel_avant_jours = models.IntegerField(db_comment='Rappel avant (jours)')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Assurance {self.vehicule} expire le {self.expiration_assurance}"

    class Meta:
        managed = False
        db_table = 'assurances'


class TaxeCirculation(models.Model):
    # CORRECTION : Ajout de related_name pour éviter le conflit avec flotte.TaxeCirculation
    vehicule = models.ForeignKey(Vehicule, models.CASCADE, related_name='taxes_maintenance')

    date_taxe_circulation = models.DateField()
    expiration = models.DateField()
    rappel_avant_jours = models.IntegerField(db_comment='Rappel avant (jours)')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Taxe {self.vehicule} expire le {self.expiration}"

    class Meta:
        managed = False
        db_table = 'taxes_circulation'
        verbose_name_plural = "Taxes de Circulation"


class VisiteTechnique(models.Model):
    # CORRECTION : Ajout de related_name pour éviter le conflit avec flotte.VisiteTechnique
    vehicule = models.ForeignKey(Vehicule, models.CASCADE, related_name='visites_maintenance')

    derniere_visite = models.DateField()
    prochaine_visite = models.DateField()
    rappel_avant_jours = models.IntegerField(db_comment='Rappel avant (jours)')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Visite {self.vehicule} prochaine: {self.prochaine_visite}"

    class Meta:
        managed = False
        db_table = 'visites_techniques'
        verbose_name_plural = "Visites Techniques"


class Anomalie(models.Model):
    # ON DELETE CASCADE
    vehicule = models.ForeignKey(Vehicule, models.CASCADE)
    conducteur = models.ForeignKey(Conducteur, models.CASCADE)

    type_anomalie = models.CharField(max_length=100, blank=True, null=True, db_comment='Mécanique, Accident, Autre')
    description = models.TextField(db_comment='Formulaire simple pour signaler un problème')
    statut = models.CharField(max_length=50, blank=True, null=True, db_comment='Signalé, En cours, Résolu')
    date_declaration = models.DateTimeField(blank=True, null=True)
    photo_path = models.CharField(max_length=255, blank=True, null=True, db_comment="Possibilité d'attacher des photos")
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Anomalie {self.id} sur {self.vehicule}"

    class Meta:
        managed = False
        db_table = 'anomalies'


class AlerteEmail(models.Model):
    email_destinataire = models.CharField(max_length=100)
    type_alerte = models.CharField(max_length=50, db_comment='assurance, taxe circulation, entretient, visite technique')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Alerte {self.type_alerte} vers {self.email_destinataire}"

    class Meta:
        managed = False
        db_table = 'alertes_email'
        verbose_name_plural = "Alertes E-mail"

