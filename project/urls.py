from django.urls import path

from project.views import MyProjectsAPI, ProjectAPI, ChangeInviteSlugProject, JoinToProject, LeaveProject, \
    PersonalizeProjectAPI

app_name = 'project'
urlpatterns = [
    path('', MyProjectsAPI.as_view(), name='projects_list'),
    path('<int:pk>/', ProjectAPI.as_view(), name='project'),
    path('<int:pk>/inviteslug/', ChangeInviteSlugProject.as_view(), name='change_invite_slug'),
    path('invite/<invite_slug>/', JoinToProject.as_view(), name='join_to_project'),
    path('<int:pk>/leave/', LeaveProject.as_view(), name='leave_project'),
    path('<int:pk>/personalize/', PersonalizeProjectAPI.as_view(), name='personalize_project'),
]
