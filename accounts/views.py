from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from accounts.forms import MyUserCreationForm
from accounts.models import Profile


class RegisterView(CreateView):
    model = User
    template_name = 'create_user.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:projects')
        return next_url


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_profile.html'
    paginate_by = 3
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.get_object().projects.all(), self.paginate_by, self.paginate_orphans)
        page_number = self.request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_object
        context['projects'] = page_object.object_list
        context['is_paginated'] = page_object.has_other_pages()
        return context


class UsersView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users_list.html'
    context_object_name = 'users'
    paginate_by = 3
    paginate_orphans = 0

    def has_permission(self):
        return self.request.user.has_perm(
            'accounts.can_view_all_users') and self.request.user in User.objects.all() or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('accounts:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator = Paginator(User.objects.exclude(username=self.request.user), self.paginate_by, self.paginate_orphans)
        page_number = self.request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_object
        context['users'] = page_object.object_list
        context['is_paginated'] = page_object.has_other_pages()
        # context['users'] = User.objects.exclude(username=self.request.user)
        return context