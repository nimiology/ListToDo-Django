from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from activity.models import Activity
from comment.models import Comment
from comment.serializers import CommentSerializer
from task.permissions import IsItUsersProjectWithSection


class CommentAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsItUsersProjectWithSection]

    def perform_update(self, serializer):
        user = self.request.user
        obj = self.get_object()
        project = obj.project
        obj = serializer.save(owner=obj.owner, project=project)
        Activity(assignee=user, project=project, comment=obj, status='U',
                 description=f'{user} edited a comment: {obj.project.title}').save()
        return obj

    def perform_destroy(self, instance):
        user = self.request.user
        project = instance.project
        Activity(assignee=user, project=project, status='D',
                 description=f'{user} deleted a comment: {instance.project.title}').save()
        return instance.delete()


class CommentListCreateAPI(ListCreateAPIView):
    serializer_class = CommentSerializer
    filterset_fields = ['project', 'task', ]

    def get_queryset(self):
        user = self.request.user
        comments = Comment.objects.filter(project__users__in=user.projects.all())
        return comments

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data.get('project')
        obj = serializer.save(owner=self.request.user, project=project)
        Activity(assignee=user, project=project, comment=obj, status='C',
                 description=f'{user} created a comment: {obj.project.title}').save()
        return obj
