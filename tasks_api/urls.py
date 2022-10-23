from django.urls import path

from tasks_api.views import ProjectAPI, MyProjectsAPI, LabelAPI, MyLabelsAPI, LeaveProject, \
    SectionAPI, CommentAPI, \
    TaskAPI, TasksAPI, SectionsAPI, CommentsAPI, ChangeInviteSlugProject, ActivityAPI, JoinToProject, \
    PersonalizeProjectAPI

app_name = 'tasks_api'
urlpatterns = [
    path('project/<int:pk>/', ProjectAPI.as_view(), name='project'),
    path('project/<int:pk>/inviteslug/', ChangeInviteSlugProject.as_view()),
    path('projects/', MyProjectsAPI.as_view()),
    path('project/invite/<inviteSlug>/', JoinToProject.as_view()),
    path('project/<int:pk>/leave/', LeaveProject.as_view()),
    path('project/<int:pk>/personalize/', PersonalizeProjectAPI.as_view()),

    path('label/<int:pk>/', LabelAPI.as_view()),
    path('labels/', MyLabelsAPI.as_view()),

    path('section/<int:pk>/', SectionAPI.as_view()),
    path('sections/', SectionsAPI.as_view()),

    path('tasks/', TasksAPI.as_view()),
    path('task/<int:pk>/', TaskAPI.as_view()),

    path('comments/', CommentsAPI.as_view()),
    path('comment/<int:pk>/', CommentAPI.as_view()),

    path('activity/', ActivityAPI.as_view()),

]
