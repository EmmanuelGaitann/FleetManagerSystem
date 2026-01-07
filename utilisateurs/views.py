# utilisateurs/views.py

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import User, Role
from .forms import CustomUserCreationForm, ChauffeurUserCreationForm
from django.shortcuts import redirect # Nécessaire pour les redirections en cas d'échec

class GestionnaireRequiredMixin(UserPassesTestMixin):
    """
    Mixin pour n'autoriser que les Superusers ou les Gestionnaires Flotte à accéder à la vue.
    """
    def test_func(self):
        # 1. Le Superuser a toujours accès
        if self.request.user.is_superuser:
            return True

        # L'utilisateur doit être connecté pour avoir un rôle
        if not self.request.user.is_authenticated:
            return False

        # 2. Vérification du rôle 'Gestionnaire Flotte'
        user_role_name = self.request.user.role.nom if hasattr(self.request.user, 'role') and self.request.user.role else None
        return user_role_name == 'Gestionnaire Flotte'

    def handle_no_permission(self):
        # Redirection vers le tableau de bord si les permissions sont insuffisantes
        return redirect('dashboard')


class UserCreateView(GestionnaireRequiredMixin, CreateView):
    """
    Vue pour créer un nouvel utilisateur via l'interface.
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'utilisateurs/user_form.html'
    success_url = reverse_lazy('dashboard') # Rediriger vers le tableau de bord après la création

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajouter un nouvel Utilisateur"
        return context

class ChauffeurCreateView(GestionnaireRequiredMixin, CreateView):
    """
    Vue pour créer un compte Chauffeur :
    - Crée un User (rôle Chauffeur/Opérateur)
    - Crée le Conducteur associé
    """
    model = User
    form_class = ChauffeurUserCreationForm
    template_name = 'utilisateurs/chauffeur_form.html'
    success_url = reverse_lazy('conducteur_list')  # On revient sur la liste des conducteurs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Créer un compte Chauffeur"
        return context
