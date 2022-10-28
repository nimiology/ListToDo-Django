from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from activity.models import Activity
from task.models import Task
from task.permissions import IsItUsersProjectWithTask
from task.serializers import TaskSerializer


class TaskAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsItUsersProjectWithTask]

    def perform_update(self, serializer):
        user = self.request.user
        obj = self.get_object()
        project = obj.section.project
        obj = serializer.save(owner=obj.owner)
        Activity(assignee=user, project=project, task=obj, status='U',
                 description=f'{user} edited a task: {obj.title}').save()
        return obj

    def perform_destroy(self, instance):
        user = self.request.user
        project = instance.section.project
        Activity(assignee=user, project=project, status='D',
                 description=f'{user} deleted a task: {instance.title}').save()
        return instance.delete()


class TaskListCreateAPI(ListCreateAPIView):
    serializer_class = TaskSerializer
    filterset_fields = {'title': ['exact'],
                        'assignee': ['exact'],
                        'section': ['exact'],
                        'task': ['exact', 'isnull'],
                        'description': ['exact'],
                        'color': ['exact'],
                        'label': ['exact'],
                        'priority': ['exact'],
                        'completed': ['exact'],
                        'created': ['exact'],
                        'schedule': ['exact'],
                        'completedDate': ['exact', 'isnull'], }

    def get_queryset(self):
        user = self.request.user
        tasks = Task.objects.filter(section__project__users__in=user.projects.all())
        return tasks

    def perform_create(self, serializer):
        user = self.request.user
        section = serializer.validated_data.get('section')
        project = section.project
        obj = serializer.save(owner=self.request.user, section=section)
        Activity.objects.create(assignee=user, project=project, task=obj, status='C',
                                description=f'{user} created a task: {obj.title}')
        return obj


