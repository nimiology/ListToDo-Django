from django.urls import path

from comment.views import CommentListCreateAPI, CommentAPI

app_name = 'comment'
urlpatterns = [
    path('', CommentListCreateAPI.as_view(), name='comment_list'),
    path('<int:pk>/', CommentAPI.as_view(), name='comment'),


]