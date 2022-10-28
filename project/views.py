from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response

from activity.models import Activity
from project.models import Project, ProjectUser
from project.serializers import ProjectSerializer, ProjectUsersSerializer4JoinProject, ProjectUsersPersonalizeSerializer
from task.permissions import IsInProject, IsOwner, IsItUsersProjectWithProject
from task.utils import slug_generator


class ProjectAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsInProject]
    queryset = Project.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        project = self.get_object()
        obj = serializer.save(owner=project.owner)
        Activity(assignee=user, project=obj, status='U', description=f'{user} edited a project: {obj.title}').save()
        return obj


class MyProjectsAPI(ListCreateAPIView):
    filterset_fields = {'project__project': ['exact', 'isnull'],
                        'project__title': ['exact'],
                        'color': ['exact'], 'label': ['exact'],
                        'project__archive': ['exact'], 'project__created': ['exact'],
                        'project__schedule': ['exact'], 'project__inbox': ['exact']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectSerializer
        else:
            return ProjectUsersSerializer4JoinProject

    def get_queryset(self):
        user = self.request.user
        return ProjectUser.objects.filter(owner=user).order_by('position')

    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(owner=user)
        Activity(assignee=user, project=obj, status='C', description=f'{user} created a project: {obj.title}').save()
        return obj


class PersonalizeProjectAPI(UpdateAPIView):
    serializer_class = ProjectUsersPersonalizeSerializer
    queryset = ProjectUser.objects.all()
    permission_classes = [IsOwner]


class JoinToProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'invite_slug'

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user
        if project.owner != user:
            try:
                ProjectUser(owner=user, project=project).save()
                return self.retrieve(request, *args, **kwargs)
            except:
                raise ValidationError("You've already joined this project!")
        else:
            raise ValidationError("You can't join to your own project!")


class LeaveProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsItUsersProjectWithProject]
    queryset = Project.objects.all()

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            try:
                project.users.get(owner=request.user).delete()
            except ProjectUser.DoesNotExist:
                raise ValidationError("You are not in this project!")
            serializer = self.get_serializer(project)
            return Response(serializer.data)

        else:
            raise ValidationError("You can't leave to your own project!")


class ChangeInviteSlugProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsItUsersProjectWithProject]
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.invite_slug = slug_generator()
        obj.save()
        return self.retrieve(request, *args, **kwargs)

