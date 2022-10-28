from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.response import Response

from activity.models import Activity
from project.models import ProjectUser
from project.serializers import ChangeProjectPositionSerializer
from section.models import Section
from section.serializers import ChangeSectionPositionSerializer
from task.models import Task
from task.permissions import IsItUsersProjectWithTask, IsItUsersProjectWithSection, IsOwner
from task.serializers import TaskSerializer, ChangeTaskPositionSerializer


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




class ChangeProjectsPositionsAPI(GenericAPIView):
    instance_class = None
    request_type = None
    def get_serializer_class(self):
        self.request_type = self.request.GET.get('type')
        if self.request_type == 'project':
            self.serializer_class = ChangeProjectPositionSerializer
            self.permission_classes = [IsOwner]
            self.instance_class = ProjectUser
        elif self.request_type == 'section':
            self.serializer_class = ChangeSectionPositionSerializer
            self.permission_classes = [IsItUsersProjectWithSection]
            self.instance_class = Section
        elif self.request_type == 'task':
            self.serializer_class = ChangeTaskPositionSerializer
            self.permission_classes = [IsItUsersProjectWithTask]
            self.instance_class = Task
        else:
            raise ValidationError('The type params must be wrong!')
        return self.serializer_class
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # ge value from serializer
        obj = serializer.validated_data.get('obj')
        position = serializer.validated_data.get('position')
        # check_object_permissions
        self.check_object_permissions(request=self.request, obj=obj)
        args = {}
        if self.request_type == 'task':
            args['section'] = obj.section
            serializer = TaskSerializer(obj)
        elif self.request_type == 'section':
            args['project'] = obj.project
            serializer = SectionSerializer(obj)
        elif self.request_type == 'project':
            args['owner'] = obj.owner
            serializer = ProjectUsersSerializer4JoinProject(obj)
        else:
            raise ValidationError('The type params must be wrong!')
        instances = self.instance_class.objects.filter(position__gte=position, **args)
        qs = self.instance_class.objects.filter(**args)

        if obj.position > position:
            instances = instances.order_by('-position')
        elif obj.position < position:
            instances = instances.order_by('position')
        else:
            raise ValidationError('wrong position!')
        last_position = qs.order_by('-position')[0].position + 2
        first_position = obj.position
        obj.position = last_position
        obj.save()
        for object in instances:
            if object != obj:
                if first_position > position:
                    object.position += 1
                elif first_position < position:
                    object.position -= 1
                object.save()
        obj.position = position
        obj.save()
        return Response(serializer.data)