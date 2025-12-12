# utilisateurs/models.py (VERSION NETTOYÉE ET FINALE)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ====================
# Modèle de Rôle
# ====================

class Role(models.Model):
    nom = models.CharField(unique=True, max_length=50, db_comment='Administrateur Système, Gestionnaire Flotte, Chauffeur/Opérateur')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        # NOTE : 'managed = False' est utilisé car vos tables existent déjà dans la base de données.
        managed = False
        db_table = 'roles'


# ====================
# Gestionnaire d'Utilisateurs Personnalisé
# ====================

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d'utilisateur doit être défini")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # Cherche ou crée le rôle d'Administrateur Système
        try:
            admin_role = Role.objects.get(nom='Administrateur Système')
        except Role.DoesNotExist:
            admin_role = Role.objects.create(nom='Administrateur Système')

        extra_fields.setdefault('role', admin_role)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(username, email, password, **extra_fields)
        return user


# ====================
# Modèle d'Utilisateur Personnalisé
# ====================

class User(AbstractBaseUser, PermissionsMixin):

    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    username = models.CharField(unique=True, max_length=100, db_comment='username/login')
    email = models.CharField(unique=True, max_length=100)

    fonction = models.CharField(max_length=100, blank=True, null=True, db_comment="Fonction de l'utilisateur")

    # NOTE : J'ai mis models.SET_NULL pour la FK role pour éviter un crash si le rôle est supprimé,
    # mais votre code utilise models.PROTECT. Je respecte votre choix initial pour éviter de casser la logique DB.
    role = models.ForeignKey(Role, models.PROTECT)

    email_verified_at = models.DateTimeField(null=True, blank=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nom', 'prenom']

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser or (self.role and self.role.nom == 'Gestionnaire Flotte')

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.nom} {self.prenom}"

    def get_short_name(self):
        return self.prenom

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.username})"

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"