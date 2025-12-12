# utilisateurs/forms.py (VERSION COMPLÈTE)

from django import forms
from .models import User

# ====================
# Formulaire de Création Utilisateur
# Utilisé pour l'Admin et pour l'inscription initiale
# ====================
class CustomUserCreationForm(forms.ModelForm):
    # Champs de mot de passe requis pour le hachage
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de Passe")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmer le Mot de Passe")

    class Meta:
        model = User
        # CORRECTION CONFIRMÉE : Utilisation de 'nom' et 'prenom'
        fields = ('username', 'prenom', 'nom', 'email', 'role', 'fonction', 'is_active', 'is_superuser', 'is_staff')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        # Utilise create_user du CustomUserManager pour hacher le mot de passe
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# ====================
# Formulaire de Modification Utilisateur
# Utilisé pour l'Admin lors de la modification d'un utilisateur existant
# ====================
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        # NOTE : Pas de champ 'password' ici
        fields = ('username', 'prenom', 'nom', 'email', 'role', 'fonction', 'is_active', 'is_superuser', 'is_staff')