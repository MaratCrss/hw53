from django.urls import path

from webapp.projects import ProjectsView, CreateProject, ProjectView
from webapp.views import TasksView, TaskView, CreateTask, UpdateView, DeleteTask, CreateTaskWithProject

urlpatterns = [
    path('', ProjectsView.as_view(), name='projects'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('task_view/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('project_view/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('create_task/', CreateTask.as_view(), name='create_task'),
    path('create_task/with_project/<int:pk>/', CreateTaskWithProject.as_view(), name='create_task_with_project'),
    path('create_project/', CreateProject.as_view(), name='create_project'),
    path('update_task/<int:pk>/', UpdateView.as_view(), name='update_task'),
    path('delete_task/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
]