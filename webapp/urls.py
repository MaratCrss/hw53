from django.urls import path

from webapp.views import TasksView, TaskView, CreateTask, UpdateView, DeleteTask

urlpatterns = [
    path('', TasksView.as_view(), name='index'),
    path('task_view/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('create_task/', CreateTask.as_view(), name='create_task'),
    path('update_task/<int:pk>/', UpdateView.as_view(), name='update_task'),
    path('delete_task/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
]