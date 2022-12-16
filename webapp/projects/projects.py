from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlencode
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
                Q(title__icontains=self.search_value) | Q(content__icontains=self.search_value))
        return ProjectModel.objects.all()

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


class CreateProject(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'projects/create_project.html'


class UpdateProject(LoginRequiredMixin,UpdateView):
    form_class = ProjectForm
    template_name = 'projects/update_project.html'
    model = ProjectModel


class DeleteProject(LoginRequiredMixin, DeleteView):
    model = ProjectModel
    context_object_name = 'project'
    template_name = 'projects/delete_project.html'
    success_url = reverse_lazy('webapp:projects')