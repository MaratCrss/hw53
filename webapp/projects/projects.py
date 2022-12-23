from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import SearchForm, ProjectForm
from webapp.models import ProjectModel


class ProjectsView(ListView):
    model = ProjectModel
    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'
    paginate_by = 5
    paginate_orphans = 2
    form = None
    search_value = None

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        if self.form.is_valid():
            self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')

    def get_queryset(self):
        if self.search_value:
            return ProjectModel.objects.filter(
                Q(title__icontains=self.search_value) |
                Q(content__icontains=self.search_value)).order_by('-title')
        return ProjectModel.objects.all().order_by('-title')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context


class ProjectView(DetailView):
    model = ProjectModel
    template_name = 'projects/project_view.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.order_by('-created_at')
        paginator = Paginator(tasks, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['tasks'] = page_obj.object_list
        context['page_obj'] = page_obj
        return context


class CreateProject(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'projects/create_project.html'
    permission_required = 'webapp.add_projectmodel'


class UpdateProject(PermissionRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = 'projects/update_project.html'
    model = ProjectModel
    permission_required = 'webapp.change_projectmodel'


class DeleteProject(PermissionRequiredMixin, DeleteView):
    model = ProjectModel
    context_object_name = 'project'
    template_name = 'projects/delete_project.html'
    success_url = reverse_lazy('webapp:projects')
    permission_required = 'webapp.delete_projectmodel'


class DeleteUserByProject(PermissionRequiredMixin, View):
    pk_url_kwarg = 'project_pk'

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(ProjectModel, pk=kwargs.get('project_pk'))
        user = get_object_or_404(User, pk=kwargs.get('user_pk'))

        context = {
            'project': project,
            'user': user
        }
        return render(request, 'projects/delete_user_by_project.html', context)

    def has_permission(self):
        project = get_object_or_404(ProjectModel, pk=self.kwargs.get('project_pk'))
        return self.request.user.has_perm('webapp.can_delete_users_to_the_project') and self.request.user in project.users.all() or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(ProjectModel, pk=kwargs.get('project_pk'))
        user = get_object_or_404(User, pk=kwargs.get('user_pk'))
        project.users.remove(user)
        return redirect('webapp:project_view', pk=project.pk)


class CreateUserProject(PermissionRequiredMixin ,CreateView):

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(ProjectModel, pk=self.kwargs.get('pk'))
        context = {
            'project': project,
            'users': User.objects.exclude(projects__id=project.id)
        }
        return render(request, 'projects/create_user_in_project.html', context)

    def has_permission(self):
        project = get_object_or_404(ProjectModel, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.can_add_users_to_the_project') and self.request.user in project.users.all() or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(ProjectModel, pk=request.POST.get('project_id'))
        user = int(request.POST.get('user_project'))
        project.users.add(user)
        return redirect('webapp:project_view', pk=project.pk)