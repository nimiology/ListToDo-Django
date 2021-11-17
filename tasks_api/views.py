from django.db.models import Q
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    UpdateAPIView, GenericAPIView
from rest_framework.response import Response

from tasks_api.models import Project, Label, Color, Section, Task, Comment, Activity, ProjectUser
from tasks_api.permissions import IsInProjectOrCreatOnly, IsItUsersProjectWithProject, \
    IsItUsersProjectWithOBJ, IsOwner
from tasks_api.serializers import ProjectSerializer, LabelSerializer, ColorSerializer, SectionSerializer, \
    TaskSerializer, CommentSerializer, ActivitySerializer, ProjectUsersSerializer4JoinProject, \
    ChangeProjectPositionSerializer
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
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['title', 'project', 'color', 'label', 'archive', 'created', 'schedule', ]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(users__in=user.projects.all())


class JoinToProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    lookup_field = 'inviteSlug'

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user
        if project.owner != user:
            try:
                print(ProjectUser.objects.get(project=project, owner=user))
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
    permission_classes = [IsAuthenticated, IsItUsersProjectWithOBJ]

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
    permission_classes = [IsAuthenticated, IsItUsersProjectWithOBJ]

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
    permission_classes = [IsAuthenticated, IsItUsersProjectWithOBJ]

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
    permission_classes = [IsAuthenticated, IsItUsersProjectWithOBJ]

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
    serializer_class = ChangeProjectPositionSerializer
    permission_classes = [IsAuthenticated & IsOwner]
    queryset = ProjectUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project1 = serializer.validated_data.get('project1')
        project2 = serializer.validated_data.get('project2')
        self.check_object_permissions(request=self.request, obj=project1)
        self.check_object_permissions(request=self.request, obj=project2)
        projects_user = ProjectUser.objects.filter(owner=project1.owner).order_by('-position')
        project_user_last = projects_user[0]
        position1 = project2.position
        position2 = project1.position
        project2.position = project_user_last.position + 1
        project2.save()
        project1.position = position1
        project1.save()
        project2.position = position2
        project2.save()
        serializer = ProjectSerializer(project1.project)
        return Response(serializer.data)

