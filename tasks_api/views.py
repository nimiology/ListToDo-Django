from django.db.models import Q
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    get_object_or_404

from tasks_api.models import Project, Label, Color, Section, Task, Comment
from tasks_api.permissions import IsOwnerOrCreatOnly, IsItOwnerOrUsersProjectWithProject, \
    IsItOwnerOrUsersProjectWithOBJ
from tasks_api.serializers import ProjectSerializer, LabelSerializer, ColorSerializer, SectionSerializer, \
    TaskSerializer, CommentSerializer
from tasks_api.utils import CreateRetrieveUpdateDestroyAPIView, check_creating_task, check_task_in_project


class ProjectsAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrCreatOnly, IsAuthenticated]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        project = self.get_object()
        return serializer.save(owner=project.owner)


class MyProjectsAPI(ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithOBJ]

    def perform_update(self, serializer):
        section = self.get_object()
        return serializer.save(project=section.project)


class ProjectSectionsAPI(ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        if self.request.user in project.users.all() or self.request.user == project.owner:
            return project.sections.all().order_by('position')
        else:
            raise NotFound


class CreateTaskAPI(CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithProject]

    def perform_create(self, serializer):
        project = self.get_object()
        check_creating_task(serializer, project, self.request.user)
        return serializer.save(owner=self.request.user, project=project)


class TaskAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithOBJ]

    def perform_update(self, serializer):
        obj = self.get_object()
        project = obj.project
        check_creating_task(serializer, project, self.request.user)
        return serializer.save(owner=obj.owner, project=obj.project)


class TasksAPI(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['title', 'assignee', 'section', 'task', 'description', 'color', 'label', 'priority', 'position',
                       'completed', 'created', 'schedule', 'completedDate', ]

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(Q(owner=user) | Q(users__in=[user]))
        objs = []

        for project in projects:
            for task in project.tasks.all():
                objs.append(task)
        return objs


class ProjectTasksAPI(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        if self.request.user in project.users.all() or self.request.user == project.owner:
            return project.tasks.all()
        else:
            raise NotFound


class CreateCommentAPI(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithProject]

    def perform_create(self, serializer):
        project = self.get_object()
        check_task_in_project(serializer, project)
        return serializer.save(owner=self.request.user, project=project)


class CommentAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsItOwnerOrUsersProjectWithOBJ]

    def perform_update(self, serializer):
        comment = self.get_object()
        check_task_in_project(serializer, comment.project)
        return serializer.save(owner=comment.owner, project=comment.project)


class ProjectCommentsAPI(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        if self.request.user in project.users.all() or self.request.user == project.owner:
            return project.comments.all().order_by('-id')
        else:
            raise NotFound


class TaskCommentsAPI(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs['pk'])
        project = task.project
        if self.request.user in project.users.all() or self.request.user == project.owner:
            return task.comments.all().order_by('-id')
        else:
            raise NotFound
