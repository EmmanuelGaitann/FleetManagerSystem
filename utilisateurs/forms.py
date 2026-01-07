from django import forms
from .models import User, Role
from flotte.models import Conducteur


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

class ChauffeurUserCreationForm(forms.ModelForm):
    """
    Formulaire dédié :
    - Crée un compte utilisateur avec le rôle 'Chauffeur/Opérateur'
    - Crée automatiquement un Conducteur associé (mêmes nom/prénom/email + infos chauffeur)
    """

    # Champs supplémentaires pour le compte
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    # Champs spécifiques au chauffeur (table Conducteurs)
    numero_permis = forms.CharField(label="Numéro de permis")
    date_naissance = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date de naissance"
    )
    date_embauche = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date d'embauche"
    )
    adresse = forms.CharField(required=False, label="Adresse / quartier")
    ville = forms.CharField(required=False, label="Ville")
    tel1 = forms.CharField(required=False, label="Téléphone principal")
    tel2 = forms.CharField(required=False, label="Téléphone secondaire")

    class Meta:
        model = User
        # On ne laisse pas choisir le rôle ici : ce sera toujours Chauffeur/Opérateur
        fields = ('username', 'prenom', 'nom', 'email')

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        pwd2 = cleaned_data.get("password_confirm")

        if pwd and pwd2 and pwd != pwd2:
            self.add_error("password_confirm", "Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        """
        1) Crée le User avec rôle 'Chauffeur/Opérateur'
        2) Crée le Conducteur correspondant
        """
        # 1. Créer l'utilisateur sans enregistrer tout de suite
        user = super().save(commit=False)

        # Rôle Chauffeur/Opérateur
        try:
            chauffeur_role = Role.objects.get(nom="Chauffeur/Opérateur")
        except Role.DoesNotExist:
            chauffeur_role = None

        user.role = chauffeur_role
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False

        # Mot de passe
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

            # 2. Créer le conducteur lié "logiquement"
            Conducteur.objects.create(
                nom=user.nom,
                prenom=user.prenom,
                date_naissance=self.cleaned_data.get("date_naissance"),
                date_embauche=self.cleaned_data.get("date_embauche"),
                numero_permis=self.cleaned_data["numero_permis"],
                adresse=self.cleaned_data.get("adresse") or "",
                ville=self.cleaned_data.get("ville") or "",
                tel1=self.cleaned_data.get("tel1") or "",
                tel2=self.cleaned_data.get("tel2") or "",
                email=user.email,
            )

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