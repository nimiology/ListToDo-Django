from django.urls import path

from label.views import MyLabelListCreateAPI, LabelAPI

app_name = 'label'
urlpatterns = [
    path('', MyLabelListCreateAPI.as_view(), name='label_list'),
    path('<int:pk>/', LabelAPI.as_view(), name='label'),

]
