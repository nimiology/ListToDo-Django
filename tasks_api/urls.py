from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks_api.views import ProjectsAPI, MyProjectsAPI, LabelAPI, MyLabelsAPI, AddToProject, ColorsAPI, \
    CreateSectionAPI, \
    SectionAPI, CreateTaskAPI, CreateCommentAPI, CommentAPI, \
    TaskAPI, TasksAPI, SectionsAPI, CommentsAPI

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
    path('section/<int:pk>/', SectionAPI.as_view()),
    path('sections/', SectionsAPI.as_view()),

    path('project/<int:pk>/task/', CreateTaskAPI.as_view()),
    path('tasks/', TasksAPI.as_view()),
    path('task/<int:pk>/', TaskAPI.as_view()),

    path('project/<int:pk>/comment/', CreateCommentAPI.as_view()),
    path('comments/', CommentsAPI.as_view()),
    path('comment/<int:pk>/', CommentAPI.as_view()),

]