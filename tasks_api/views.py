from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from tasks_api.models import Project, Label, Color, Section, Task, Comment, Activity
from tasks_api.permissions import IsInProjectOrCreatOnly, IsItOwnerOrUsersProjectWithProject, \
    IsItOwnerOrUsersProjectWithOBJ
from tasks_api.serializers import ProjectSerializer, LabelSerializer, ColorSerializer, SectionSerializer, \
    TaskSerializer, CommentSerializer, ActivitySerializer
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
        return Project.objects.filter(Q(owner=user) | Q(users__in=[user])).order_by('position')


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


class ChangeInviteSlugProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithProject]
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
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithProject]

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
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithOBJ]

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
    filterset_fields = ['title', 'project', 'position', 'archive', ]

    def get_queryset(self):
        user = self.request.user
        sections = Section.objects.filter(Q(project__owner=user) | Q(project__users__in=[user])).order_by('position')
        return sections


class CreateTaskAPI(CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithProject]

    def perform_create(self, serializer):
        user = self.request.user
        project = self.get_object()
        check_creating_task(serializer, project, self.request.user)
        obj = serializer.save(owner=self.request.user, project=project)
        Activity(assignee=user, project=project, task=obj, status='C',
                 description=f'{user} created a task: {obj.title}').save()
        return obj


class TaskAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithOBJ]

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
    filterset_fields = ['title', 'assignee', 'section', 'task', 'description', 'color', 'label', 'priority', 'position',
                        'completed', 'created', 'schedule', 'completedDate', ]

    def get_queryset(self):
        user = self.request.user
        tasks = Task.objects.filter(Q(project__owner=user) | Q(project__users__in=[user]))
        return tasks


class CreateCommentAPI(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithProject]

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
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithOBJ]

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
        comments = Comment.objects.filter(Q(project__owner=user) | Q(project__users__in=[user]))
        return comments


class ActivityAPI(ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['assignee', 'project', 'section', 'task', 'comment', 'status', ]

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(Q(project__owner=user) | Q(project__users__in=[user]))