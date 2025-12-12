# fournisseurs/models.py (Contenu complet)

from django.db import models

# ====================
# Modèles : Fournisseurs & Pièces
# ====================

class Fournisseur(models.Model):
    # Liste de choix suggérée pour le formulaire (à placer dans forms.py ou ici)
    ACTIVITE_CHOICES = [
        ('vente_vehicule', 'Vente de Véhicules'),
        ('location_vehicule', 'Location de Véhicules'),
        ('assureur', 'Assureur'),
        ('vente_piece_auto', 'Vente de Pièces Auto'),
        ('entretien', 'Entretien et Réparation'),
        ('reparation', 'Réparation'),
        ('vente_carburant', 'Vente de Carburant'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=255)
    type_activite = models.CharField(max_length=255, db_comment='vente vehicule, location vehicule, assureur, vente pièce auto, entretien, reparation, vente carburant')
    contact = models.CharField(max_length=255, blank=True, null=True)
    tel1 = models.CharField(max_length=20, blank=True, null=True)
    tel2 = models.CharField(max_length=20, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    site_web = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    type_fournisseur = models.CharField(max_length=50, blank=True, null=True, db_comment='Type (à affiner si nécessaire)')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        managed = False
        db_table = 'fournisseurs'


class Piece(models.Model):
    # ON DELETE SET NULL
    fournisseur = models.ForeignKey(Fournisseur, models.SET_NULL, blank=True, null=True)

    constructeur = models.CharField(max_length=150, blank=True, null=True, db_comment='Constructeur de la pièce')
    numero = models.CharField(max_length=150, db_comment='Numéro de la pièce')
    nom = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2, db_comment='Prix unitaire')
    date_prix = models.DateField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} ({self.numero})"

    class Meta:
        managed = False
        db_table = 'pieces'