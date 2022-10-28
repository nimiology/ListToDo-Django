from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from activity.models import Activity
from section.models import Section
from section.serializers import SectionSerializer
from task.permissions import IsItUsersProjectWithSection


class SectionAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [IsItUsersProjectWithSection]

    def perform_update(self, serializer):
        user = self.request.user
        section = self.get_object()
        project = section.project
        obj = serializer.save(project=project)
        Activity(assignee=user, project=project, section=obj, status='U',
                 description=f'{user} edited a section: {obj.title}').save()
        return obj

    def perform_destroy(self, instance):
        user = self.request.user
        project = instance.project
        Activity(assignee=user, project=project, status='D',
                 description=f'{user} deleted a section: {instance.title}').save()
        return instance.delete()


class SectionListCreateAPI(ListCreateAPIView):
    serializer_class = SectionSerializer
    filterset_fields = ['title', 'project', 'archive', ]

    def get_queryset(self):
        user = self.request.user
        sections = Section.objects.filter(project__users__in=user.projects.all())
        return sections

    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save()
        Activity(assignee=user, project=obj.project, section=obj, status='C',
                 description=f'{user} created a section: {obj.title}').save()
        return obj
