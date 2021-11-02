from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks_api.views import ProjectsAPI, MyProjectsAPI, LabelAPI, MyLabelsAPI, AddToProject, ColorsAPI, CreateSectionAPI, \
    SectionAPI, ProjectSectionsAPI

urlpatterns = [
    path('project/', ProjectsAPI.as_view()),
    path('project/<int:pk>/', ProjectsAPI.as_view()),
    path('projects/', MyProjectsAPI.as_view()),
    path('project/invite/<inviteSlug>/', AddToProject.as_view()),

    path('label/', LabelAPI.as_view()),
    path('label/<int:pk>/', LabelAPI.as_view()),
    path('labels/', MyLabelsAPI.as_view()),

    path('colors/', ColorsAPI.as_view()),

    path('project/<int:pk>/section/', CreateSectionAPI.as_view()),
    path('project/<int:pk>/sections/', ProjectSectionsAPI.as_view()),
    path('section/<int:pk>/', SectionAPI.as_view()),
]