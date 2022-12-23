from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from webapp.forms import TaskForm, SearchForm, TaskWithProjectForm
from webapp.models import IssueModel, ProjectModel


class TasksView(ListView):
    model = IssueModel
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    ordering = ('-updated_at',)
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
            return IssueModel.objects.filter(
                Q(title__icontains=self.search_value) | Q(content__icontains=self.search_value))
        return IssueModel.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context


class TaskView(DetailView):
    model = IssueModel
    template_name = 'tasks/task_view.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateTask(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/create_task.html'


class CreateTaskWithProject(PermissionRequiredMixin, CreateView):
    form_class = TaskWithProjectForm
    template_name = 'tasks/create_task_with_project.html'

    def form_valid(self, form):
        project = get_object_or_404(ProjectModel, pk=self.kwargs.get('pk'))
        user = self.request.user
        form.instance.project = project
        form.instance.users = user
        return super().form_valid(form)

    def has_permission(self):
        project= get_object_or_404(ProjectModel, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.add_issuemodel') and self.request.user in project.users.all()

    def handle_no_permission(self):
        return redirect('accounts:login')

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})


class UpdateTask(PermissionRequiredMixin, UpdateView):
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    model = IssueModel

    def has_permission(self):
        task= get_object_or_404(IssueModel, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.change_issuemodel') and self.request.user in task.project.users.all()

    def handle_no_permission(self):
        return redirect('accounts:login')


class DeleteTask(PermissionRequiredMixin, DeleteView):
    model = IssueModel
    context_object_name = 'task'
    template_name = 'tasks/delete_task.html'

    def has_permission(self):
        task= get_object_or_404(IssueModel, pk=self.kwargs.get('pk'))
        return self.request.user.has_perm('webapp.delete_issuemodel') and self.request.user in task.project.users.all()

    def handle_no_permission(self):
        return redirect('accounts:login')

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})