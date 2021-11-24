from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    GenericAPIView
from rest_framework.response import Response

from tasks_api.models import Project, Label, Color, Section, Task, Comment, Activity, ProjectUser
from tasks_api.permissions import IsInProjectOrCreatOnly, IsItUsersProjectWithProject, \
    IsItUsersProjectWithSection, IsOwner, IsItUsersProjectWithTask
from tasks_api.serializers import ProjectSerializer, LabelSerializer, ColorSerializer, SectionSerializer, \
    TaskSerializer, CommentSerializer, ActivitySerializer, ProjectUsersSerializer4JoinProject, \
    ChangeProjectPositionSerializer, ChangeTaskPositionSerializer, ChangeSectionPositionSerializer

from tasks_api.utils import CreateRetrieveUpdateDestroyAPIView, check_creating_task, check_task_in_project, \
    slug_genrator


class ProjectsAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsInProjectOrCreatOnly, IsAuthenticated]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(owner=user)
        Activity(assignee=user, project=obj, status='C').save()
        return obj

    def perform_update(self, serializer):
        user = self.request.user
        project = self.get_object()
        obj = serializer.save(owner=project.owner)
        Activity(assignee=user, project=obj, status='U').save()
        return obj


class MyProjectsAPI(ListAPIView):
    serializer_class = ProjectUsersSerializer4JoinProject
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project__title', 'project__project',
                        'project__color', 'project__label',
                        'project__archive', 'project__created',
                        'project__schedule', ]

    def get_queryset(self):
        user = self.request.user
        return ProjectUser.objects.filter(owner=user).order_by('position')


class JoinToProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    lookup_field = 'inviteSlug'

    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user
        if project.owner != user:
            try:
                ProjectUser.objects.get(project=project, owner=user)
                raise ValidationError("You've already joined this project!")
            except ProjectUser.DoesNotExist:
                ProjectUser(owner=user, project=project).save()
                return self.retrieve(request, *args, **kwargs)
        else:
            raise ValidationError("You can't join to your own project!")


class LeaveProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsItUsersProjectWithProject]
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            project.users.remove(request.user)
            serializer = self.get_serializer(project)
            return Response(serializer.data)

        else:
            raise ValidationError("You can't leave to your own project!")


class ChangeInviteSlugProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsItUsersProjectWithProject]
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.inviteSlug = slug_genrator()
        obj.save()
        return self.retrieve(request, *args, **kwargs)


class LabelAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    permission_classes = [IsInProjectOrCreatOnly, IsAuthenticated]
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
    permission_classes = [IsAuthenticated, IsItUsersProjectWithProject]

    def perform_create(self, serializer):
        user = self.request.user
        project = self.get_object()
        obj = serializer.save(project=project)
        Activity(assignee=user, project=project, section=obj, status='C',
                 description=f'{user} created a section: {obj.title}').save()
        return obj


class SectionAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [IsAuthenticated, IsItUsersProjectWithSection]

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


class SectionsAPI(ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['title', 'project', 'archive', ]

    def get_queryset(self):
        user = self.request.user
        sections = Section.objects.filter(project__users__in=user.projects.all())
        return sections


class CreateTaskAPI(CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Section.objects.all()
    permission_classes = [IsAuthenticated, IsItUsersProjectWithSection]

    def perform_create(self, serializer):
        user = self.request.user
        section = self.get_object()
        project = section.project
        check_creating_task(serializer, project, self.request.user)
        obj = serializer.save(owner=self.request.user, section=section)
        Activity(assignee=user, project=project, task=obj, status='C',
                 description=f'{user} created a task: {obj.title}').save()
        return obj


class TaskAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsItUsersProjectWithTask]

    def perform_update(self, serializer):
        user = self.request.user
        obj = self.get_object()
        project = obj.project
        check_creating_task(serializer, project, self.request.user)
        obj = serializer.save(owner=obj.owner, project=project)
        Activity(assignee=user, project=project, task=obj, status='U',
                 description=f'{user} edited a task: {obj.title}').save()
        return obj

    def perform_destroy(self, instance):
        user = self.request.user
        project = instance.project
        Activity(assignee=user, project=project, status='D',
                 description=f'{user} deleted a task: {instance.title}').save()
        return instance.delete()


class TasksAPI(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['title', 'assignee', 'section', 'task', 'description', 'color', 'label', 'priority',
                        'completed', 'created', 'schedule', 'completedDate', ]

    def get_queryset(self):
        user = self.request.user
        tasks = Task.objects.filter(section__project__users__in=user.projects.all())
        return tasks


class CreateCommentAPI(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsItUsersProjectWithProject]

    def perform_create(self, serializer):
        user = self.request.user
        project = self.get_object()
        check_task_in_project(serializer, project)
        obj = serializer.save(owner=self.request.user, project=project)
        Activity(assignee=user, project=project, comment=obj, status='C',
                 description=f'{user} created a comment: {obj.project.title}').save()
        return obj


class CommentAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsItUsersProjectWithSection]

    def perform_update(self, serializer):
        user = self.request.user
        obj = self.get_object()
        project = obj.project
        check_task_in_project(serializer, obj.project)
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


class CommentsAPI(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['project', 'task', ]

    def get_queryset(self):
        user = self.request.user
        comments = Comment.objects.filter(project__users__in=user.projects.all())
        return comments


class ActivityAPI(ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['assignee', 'project', 'section', 'task', 'comment', 'status', ]

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(project__users__in=user.projects.all())


class ChangeProjectsPositionsAPI(GenericAPIView):
    def post(self, request, *args, **kwargs):
        request_to_model = request.GET.get('type')
        if request_to_model == 'project':
            self.serializer_class = ChangeProjectPositionSerializer
            self.permission_classes = [IsAuthenticated & IsOwner]
        elif request_to_model == 'section':
            self.serializer_class = ChangeSectionPositionSerializer
            self.permission_classes = [IsAuthenticated & IsItUsersProjectWithSection]
        elif request_to_model == 'task':
            self.serializer_class = ChangeTaskPositionSerializer
            self.permission_classes = [IsAuthenticated & IsItUsersProjectWithTask]
        else:
            raise ValidationError('The type params must be wrong!')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj1 = serializer.validated_data.get('obj1')
        obj2 = serializer.validated_data.get('obj2')
        self.check_object_permissions(request=self.request, obj=obj1)
        self.check_object_permissions(request=self.request, obj=obj2)
        position1 = obj2.position
        position2 = obj1.position
        obj2.position = None
        obj2.save()
        obj1.position = position1
        obj1.save()
        obj2.position = position2
        obj2.save()
        if request_to_model == 'project':
            serializer = ProjectSerializer(obj1)
        elif request_to_model == 'section':
            serializer = SectionSerializer(obj1)
        elif request_to_model == 'task':
            serializer = TaskSerializer(obj1)
        else:
            raise ValidationError('The type params must be wrong!')
        return Response(serializer.data)
