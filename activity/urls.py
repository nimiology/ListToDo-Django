from django.urls import path

from activity.views import ActivityAPI

app_name = 'activity'
urlpatterns = [
    path('', ActivityAPI.as_view(), name='activity'),
]
