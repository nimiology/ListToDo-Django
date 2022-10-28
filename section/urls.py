from django.urls import path

from section.views import SectionListCreateAPI, SectionAPI

app_name = 'section'
urlpatterns = [
    path('<int:pk>/', SectionAPI.as_view(), name='section'),
    path('', SectionListCreateAPI.as_view(), name='section_list'),
]
