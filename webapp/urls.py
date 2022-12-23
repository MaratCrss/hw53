from django.urls import path

from webapp.projects import ProjectsView, CreateProject, ProjectView, UpdateProject, DeleteProject, CreateUserProject, \
    DeleteUserByProject
from webapp.views import TasksView, TaskView, CreateTask, UpdateTask, DeleteTask, CreateTaskWithProject

app_name = 'webapp'

urlpatterns = [
    path('', ProjectsView.as_view(), name='projects'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('task_view/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('project_view/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('task/create_task/', CreateTask.as_view(), name='create_task'),
    path('create_task/with_project/<int:pk>/', CreateTaskWithProject.as_view(), name='create_task_with_project'),
    path('project/create_project/', CreateProject.as_view(), name='create_project'),
    path('task/update_task/<int:pk>/', UpdateTask.as_view(), name='update_task'),
    path('project/update_project/<int:pk>/', UpdateProject.as_view(), name='update_project'),
    path('task/delete_task/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
    path('project/delete_project/<int:pk>/', DeleteProject.as_view(), name='delete_project'),
    path('project/add_user/<int:pk>/', CreateUserProject.as_view(), name='add_user'),
    path('project/delete_user/project_id/<int:project_pk>/user_id/<int:user_pk>/', DeleteUserByProject.as_view(), name='delete_user'),
]