from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView

from tasks.models import Project, Label
from tasks.permissions import IsOwnerOrCreatOnly
from tasks.serializers import ProjectSerializer, LabelSerializer
from tasks.utils import CreateRetrieveUpdateDestroyAPIView


class ProjectsAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrCreatOnly, IsAuthenticated]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(owner=self.get_object().owner)


class MyProjectsAPI(ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class AddToProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    lookup_field = 'inviteSlug'

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            project.user.add(request.user)
            return self.retrieve(request, *args, **kwargs)
        else:
            raise ValidationError("You can't join to your own project!")


class LabelAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    permission_classes = [IsOwnerOrCreatOnly, IsAuthenticated]
    queryset = Label.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(owner=self.get_object().owner)


class MyLabelsAPI(ListAPIView):
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user)