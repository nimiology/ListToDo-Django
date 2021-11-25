from django.conf.urls import url
from django.urls import path, include

from users.views import SettingAPI, TeamAPI, JoinTeamAPI, LeaveTeamAPI, AllTeamsAPI, ChangeInviteSlugTeam, \
    GetAllTimeZonesAPI

urlpatterns = [
    url('auth/', include('djoser.urls')),
    url('auth/', include('djoser.urls.jwt')),

    path('setting/', SettingAPI.as_view()),
    path('timezones/', GetAllTimeZonesAPI.as_view()),

    path('team/', TeamAPI.as_view()),
    path('teams/', AllTeamsAPI   .as_view()),
    path('team/<int:pk>/', TeamAPI.as_view()),
    path('team/invite/<inviteSlug>/', JoinTeamAPI.as_view()),
    path('team/<int:pk>/leave/', LeaveTeamAPI.as_view()),
    path('team/<int:pk>/inviteslug/', ChangeInviteSlugTeam.as_view()),

]