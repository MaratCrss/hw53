from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from accounts.forms import MyUserCreationForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeForm
from accounts.models import Profile


class RegisterView(CreateView):
    model = get_user_model
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
    context_object_name = 'user_object'

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
            'auth.view_user') and self.request.user in User.objects.all() or self.request.user.is_superuser

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
        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'update_profile_user.html'
    profile_form_class = ProfileUpdateForm
    object = None
    context_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form_class(instance=self.get_object().profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        profile_form = self.profile_form_class(instance=self.object.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        return redirect('accounts:user_profile', pk=self.object.pk)

    def form_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))


class ChangePasswordView(UpdateView):
    model = get_user_model()
    form_class = PasswordChangeForm
    template_name = 'update_password_user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:user_profile', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        result = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return result