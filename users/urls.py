from django.conf.urls import url
from django.urls import path, include

from users.views import MyUsersAPI, TeamAPI, JoinTeamAPI, LeaveTeamAPI, TeamListCreateAPI, ChangeInviteSlugTeam, \
    GetAllTimeZonesAPI

app_name = 'users'
urlpatterns = [
    url('auth/', include('djoser.urls')),
    url('auth/', include('djoser.urls.jwt')),

    path('myinfo/', MyUsersAPI.as_view(), name='my_info'),
    path('timezones/', GetAllTimeZonesAPI.as_view(), name='timezones'),

    path('teams/', TeamListCreateAPI.as_view(), name='team_list_create'),
    path('team/<int:pk>/', TeamAPI.as_view(), name='team'),
    path('team/invite/<inviteSlug>/', JoinTeamAPI.as_view(), name='join_team'),
    path('team/<int:pk>/leave/', LeaveTeamAPI.as_view()),
    path('team/<int:pk>/inviteslug/', ChangeInviteSlugTeam.as_view()),

]
