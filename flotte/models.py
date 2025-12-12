from django.db import models

# ====================
# Modèles : Flotte (Départements, Conducteurs, Véhicules, Affectations)
# ====================

class Departement(models.Model):
    nom = models.CharField(unique=True, max_length=150)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        managed = False
        db_table = 'departements'


class Conducteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(blank=True, null=True)
    date_embauche = models.DateField(blank=True, null=True)
    numero_permis = models.CharField(unique=True, max_length=50)
    adresse = models.CharField(max_length=255, blank=True, null=True, db_comment='Adresse/quartier')
    ville = models.CharField(max_length=100, blank=True, null=True)
    tel1 = models.CharField(max_length=20, blank=True, null=True)
    tel2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.numero_permis})"

    class Meta:
        managed = False
        db_table = 'conducteurs'


class Vehicule(models.Model):
    matricule = models.CharField(unique=True, max_length=50, db_comment="Plaque d'immatriculation")
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    couleur = models.CharField(max_length=50, blank=True, null=True)
    numero_serie = models.CharField(unique=True, max_length=150, blank=True, null=True, db_comment='N* Série')
    date_mise_circulation = models.DateField(blank=True, null=True, db_comment='Année')
    type_vehicule = models.CharField(max_length=50, blank=True, null=True, db_comment='4x4, berline, citadine, coupé, etc.')
    type_carburant = models.CharField(max_length=50, blank=True, null=True, db_comment='essence, diesel, etc.')
    kilometrage_initial = models.IntegerField(blank=True, null=True, db_comment='Kilométrage initial')

    # Le champ BOOLEAN MySQL 'actif' est mappé à IntegerField (0 ou 1)
    actif = models.IntegerField(blank=True, null=True, db_comment='Véhicule actif ou pas')

    # ON DELETE SET NULL
    departement = models.ForeignKey(Departement, models.SET_NULL, blank=True, null=True)

    # Le champ BOOLEAN MySQL 'location_oui_non' est mappé à IntegerField (0 ou 1)
    location_oui_non = models.IntegerField(blank=True, null=True, db_comment='Gestion des achats/location')

    date_achat_location = models.DateField(blank=True, null=True, db_comment='date achat/location')
    prix_achat_location = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_comment='prix achat/location')
    expiration_garantie = models.DateField(blank=True, null=True)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_comment='prix vente (si revendu)')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.matricule})"

    class Meta:
        managed = False
        db_table = 'vehicules'


class Affectation(models.Model):
    # ON DELETE CASCADE
    vehicule = models.ForeignKey(Vehicule, models.CASCADE)
    conducteur = models.ForeignKey(Conducteur, models.CASCADE)

    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'affectations'
        unique_together = (('vehicule', 'conducteur', 'date_debut'),)
        verbose_name_plural = "Affectations"


# ==========================================================
# Modèles : Rappels (CORRIGÉ selon fms.sql)
# ==========================================================
# Utilise 'fournisseurs.Fournisseur' si les deux apps ne sont pas le même.

class Assurance(models.Model):
    vehicule = models.ForeignKey('Vehicule', models.CASCADE)
    # Assumant que le modèle Fournisseur est accessible via 'fournisseurs.Fournisseur'
    fournisseur = models.ForeignKey('fournisseurs.Fournisseur', models.SET_NULL, blank=True, null=True, db_column='fournisseur_id')

    date_assurance = models.DateField(db_column='date_assurance')
    expiration_assurance = models.DateField(db_column='expiration_assurance')

    # Champ crucial pour l'alerte
    rappel_avant_jours = models.IntegerField(db_column='rappel_avant_jours')

    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Assurance pour {self.vehicule.matricule} (Expire le {self.expiration_assurance})"

    class Meta:
        managed = False
        db_table = 'assurances'
        verbose_name_plural = "Assurances"


class TaxeCirculation(models.Model):
    vehicule = models.ForeignKey('Vehicule', models.CASCADE)

    date_taxe_circulation = models.DateField(db_column='date_taxe_circulation')
    expiration = models.DateField(db_column='expiration') # Le champ est nommé 'expiration' dans la BDD

    # Champ crucial pour l'alerte
    rappel_avant_jours = models.IntegerField(db_column='rappel_avant_jours')

    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Taxe Circ. pour {self.vehicule.matricule} (Expire le {self.expiration})"

    class Meta:
        managed = False
        db_table = 'taxes_circulation'
        verbose_name = "Taxe de Circulation"
        verbose_name_plural = "Taxes de Circulation"


class VisiteTechnique(models.Model):
    vehicule = models.ForeignKey('Vehicule', models.CASCADE)

    derniere_visite = models.DateField(db_column='derniere_visite')
    prochaine_visite = models.DateField(db_column='prochaine_visite') # Le champ est nommé 'prochaine_visite' dans la BDD

    # Champ crucial pour l'alerte
    rappel_avant_jours = models.IntegerField(db_column='rappel_avant_jours')

    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Visite Tech. pour {self.vehicule.matricule} (Prochaine le {self.prochaine_visite})"

    class Meta:
        managed = False
        db_table = 'visites_techniques'
        verbose_name = "Visite Technique"
        verbose_name_plural = "Visites Techniques"