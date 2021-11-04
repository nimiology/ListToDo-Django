from django.conf.urls import url
from django.urls import path, include

from users.views import SettingAPI

urlpatterns = [
    url('auth/', include('djoser.urls')),
    url('auth/', include('djoser.urls.jwt')),
    path('setting/', SettingAPI.as_view()),
]