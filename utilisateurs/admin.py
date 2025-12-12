# utilisateurs/admin.py (VERSION CORRIGÉE)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserAdmin(BaseUserAdmin):
    # Les formes pour l'ajout et la modification
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Champs à afficher dans la liste (Admin List View)
    list_display = ('username', 'email', 'prenom', 'nom', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    search_fields = ('username', 'email', 'nom', 'prenom')
    ordering = ('username',)

    # Définition des groupes de champs pour la page de MODIFICATION d'utilisateur
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations Personnelles', {'fields': ('prenom', 'nom', 'email', 'fonction')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates Importantes', {'fields': ('last_login', 'created_at')}),
    )

    # Définition des groupes de champs pour la page d'AJOUT d'utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # Utilise les champs définis dans CustomUserCreationForm
            'fields': ('username', 'prenom', 'nom', 'email', 'fonction', 'role', 'password', 'password_confirm', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Suppression du get_form car il n'est pas nécessaire ici, les classes 'form' et 'add_form' suffisent
    # def get_form(self, request, obj=None, **kwargs):
    #     if obj is None:
    #         return self.add_form
    #     return self.form


# ====================
# Enregistrement des Modèles (AU NIVEAU DU MODULE)
# ====================

# Enregistrer le modèle User avec la classe Admin personnalisée
admin.site.register(User, UserAdmin)

# Enregistrer également le modèle Role
admin.site.register(Role)