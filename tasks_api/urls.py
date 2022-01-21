from django.urls import path

from tasks_api.views import ProjectsAPI, MyProjectsAPI, LabelAPI, MyLabelsAPI, LeaveProject, \
    CreateSectionAPI, SectionAPI, CreateTaskAPI, CreateCommentAPI, CommentAPI, \
    TaskAPI, TasksAPI, SectionsAPI, CommentsAPI, ChangeInviteSlugProject, ActivityAPI, JoinToProject, \
    ChangeProjectsPositionsAPI

urlpatterns = [
    path('project/', ProjectsAPI.as_view()),
    path('project/<int:pk>/', ProjectsAPI.as_view()),
    path('project/<int:pk>/inviteslug/', ChangeInviteSlugProject.as_view()),
    path('projects/', MyProjectsAPI.as_view()),
    path('project/invite/<inviteSlug>/', JoinToProject.as_view()),
    path('project/<int:pk>/leave/', LeaveProject.as_view()),

    path('label/', LabelAPI.as_view()),
    path('label/<int:pk>/', LabelAPI.as_view()),
    path('labels/', MyLabelsAPI.as_view()),

    path('project/<int:pk>/section/', CreateSectionAPI.as_view()),
    path('section/<int:pk>/', SectionAPI.as_view()),
    path('sections/', SectionsAPI.as_view()),

    path('section/<int:pk>/task/', CreateTaskAPI.as_view()),
    path('tasks/', TasksAPI.as_view()),
    path('task/<int:pk>/', TaskAPI.as_view()),

    path('project/<int:pk>/comment/', CreateCommentAPI.as_view()),
    path('comments/', CommentsAPI.as_view()),
    path('comment/<int:pk>/', CommentAPI.as_view()),

    path('activity/', ActivityAPI.as_view()),

    path('changeposition/', ChangeProjectsPositionsAPI.as_view()),

]