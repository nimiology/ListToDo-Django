from django.urls import path

from task.views import TaskAPI, TaskListCreateAPI

app_name = 'task'
urlpatterns = [
    path('tasks/', TaskListCreateAPI.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskAPI.as_view(), name='task'),
]
