from django.urls import path

from task.views import ProjectAPI, MyProjectsAPI, LabelAPI, MyLabelsAPI, LeaveProject, \
    SectionAPI, CommentAPI, \
    TaskAPI, TasksAPI, SectionsAPI, CommentsAPI, ChangeInviteSlugProject, ActivityAPI, JoinToProject, \
    PersonalizeProjectAPI

app_name = 'tasks'
urlpatterns = [
    path('projects/', MyProjectsAPI.as_view(), name='projects_list'),
    path('project/<int:pk>/', ProjectAPI.as_view(), name='project'),
    path('project/<int:pk>/inviteslug/', ChangeInviteSlugProject.as_view(), name='change_invite_slug'),
    path('project/invite/<invite_slug>/', JoinToProject.as_view(), name='join_to_project'),
    path('project/<int:pk>/leave/', LeaveProject.as_view(), name='leave_project'),
    path('project/<int:pk>/personalize/', PersonalizeProjectAPI.as_view(), name='personalize_project'),

    path('label/<int:pk>/', LabelAPI.as_view(), name='label'),
    path('labels/', MyLabelsAPI.as_view(), name='label_list'),

    path('section/<int:pk>/', SectionAPI.as_view()),
    path('sections/', SectionsAPI.as_view()),

    path('tasks/', TasksAPI.as_view()),
    path('task/<int:pk>/', TaskAPI.as_view()),

    path('comments/', CommentsAPI.as_view()),
    path('comment/<int:pk>/', CommentAPI.as_view()),

    path('activity/', ActivityAPI.as_view()),

]
