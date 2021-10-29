from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks.views import ProjectsAPI


urlpatterns = [
    path('project/', ProjectsAPI.as_view()),
    path('project/<int:pk>/', ProjectsAPI.as_view()),
]