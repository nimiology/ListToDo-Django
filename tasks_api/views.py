from django.db.models import Q
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView, get_object_or_404

from tasks_api.models import Project, Label, Color, Section
from tasks_api.permissions import IsOwnerOrCreatOnly, IsItOwnerOrUsersProjectWithProject, IsItOwnerOrUsersProjectWithSection
from tasks_api.serializers import ProjectSerializer, LabelSerializer, ColorSerializer, SectionSerializer
from tasks_api.utils import CreateRetrieveUpdateDestroyAPIView


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


class ColorsAPI(ListAPIView):
    serializer_class = ColorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Color.objects.all()


class CreateSectionAPI(CreateAPIView):
    serializer_class = SectionSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithProject]

    def perform_create(self, serializer):
        return serializer.save(project=self.get_object())


class SectionAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithSection]

    def perform_update(self, serializer):
        section = self.get_object()
        return serializer.save(project=section.project)


class ProjectSectionsAPI(ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        if self.request.user in project.users.all() or self.request.user == project.owner:
            return project.sections.all()
        else:
            raise NotFound
