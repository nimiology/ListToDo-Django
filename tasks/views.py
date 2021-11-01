from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView

from tasks.models import Project, Label
from tasks.permissions import IsOwnerOrCreatOnly
from tasks.serializers import ProjectSerializer, LabelSerializer
from tasks.utils import CreateRetrieveUpdateDestroyAPIView


class ProjectsAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrCreatOnly]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(owner=self.request.user)
        else:
            raise AuthenticationFailed

    def perform_update(self, serializer):
        return serializer.save(owner=self.get_object().owner)


class MyProjectsAPI(ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Project.objects.filter(owner=self.request.user)
        else:
            raise AuthenticationFailed


class LabelAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    permission_classes = [IsOwnerOrCreatOnly]
    queryset = Label.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(owner=self.request.user)
        else:
            raise AuthenticationFailed

    def perform_update(self, serializer):
        return serializer.save(owner=self.get_object().owner)


class MyLabelsAPI(ListAPIView):
    serializer_class = LabelSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Label.objects.filter(owner=self.request.user)
        else:
            raise AuthenticationFailed
