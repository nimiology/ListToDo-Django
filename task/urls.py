from django.urls import path

from task.views import TaskAPI, TaskListCreateAPI

app_name = 'task'
urlpatterns = [
    path('', TaskListCreateAPI.as_view(), name='task_list'),
    path('<int:pk>/', TaskAPI.as_view(), name='task'),
]
