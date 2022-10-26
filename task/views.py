from requests.compat import basestring
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
     UpdateAPIView, ListCreateAPIView
from rest_framework.response import Response

from task.models import Project, Label, Section, Task, Comment, Activity, ProjectUser
from task.permissions import IsInProject, IsItUsersProjectWithProject, \
    IsItUsersProjectWithSection, IsOwner, IsItUsersProjectWithTask, IsOwnerOrCreatOnly
from task.serializers import ProjectSerializer, LabelSerializer, SectionSerializer, \
    TaskSerializer, CommentSerializer, ActivitySerializer, ProjectUsersSerializer4JoinProject, \
    ProjectUsersPersonalizeSerializer, ActivityLiteSerializer

from task.utils import slug_generator


class ProjectAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsInProject]
    queryset = Project.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        project = self.get_object()
        obj = serializer.save(owner=project.owner)
        Activity(assignee=user, project=obj, status='U', description=f'{user} edited a project: {obj.title}').save()
        return obj


class MyProjectsAPI(ListCreateAPIView):
    filterset_fields = {'project__project': ['exact', 'isnull'],
                        'project__title': ['exact'],
                        'color': ['exact'], 'label': ['exact'],
                        'project__archive': ['exact'], 'project__created': ['exact'],
                        'project__schedule': ['exact'], 'project__inbox': ['exact']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectSerializer
        else:
            return ProjectUsersSerializer4JoinProject

    def get_queryset(self):
        user = self.request.user
        return ProjectUser.objects.filter(owner=user).order_by('position')

    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(owner=user)
        Activity(assignee=user, project=obj, status='C', description=f'{user} created a project: {obj.title}').save()
        return obj


class PersonalizeProjectAPI(UpdateAPIView):
    serializer_class = ProjectUsersPersonalizeSerializer
    queryset = ProjectUser.objects.all()
    permission_classes = [IsOwner]


class JoinToProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'invite_slug'

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user
        if project.owner != user:
            try:
                ProjectUser(owner=user, project=project).save()
                return self.retrieve(request, *args, **kwargs)
            except:
                raise ValidationError("You've already joined this project!")
        else:
            raise ValidationError("You can't join to your own project!")


class LeaveProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsItUsersProjectWithProject]
    queryset = Project.objects.all()

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            try:
                project.users.get(owner=request.user).delete()
            except ProjectUser.DoesNotExist:
                raise ValidationError("You are not in this project!")
            serializer = self.get_serializer(project)
            return Response(serializer.data)

        else:
            raise ValidationError("You can't leave to your own project!")


class ChangeInviteSlugProject(RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsItUsersProjectWithProject]
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.invite_slug = slug_generator()
        obj.save()
        return self.retrieve(request, *args, **kwargs)


class LabelAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    permission_classes = [IsOwnerOrCreatOnly]
    queryset = Label.objects.all()

    def perform_update(self, serializer):
        return serializer.save(owner=self.get_object().owner)


class MyLabelsAPI(ListCreateAPIView):
    serializer_class = LabelSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user)


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


class SectionsAPI(ListAPIView):
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


class TasksAPI(ListCreateAPIView):
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


class CommentAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsItUsersProjectWithSection]

    def perform_update(self, serializer):
        user = self.request.user
        obj = self.get_object()
        project = obj.project
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


class CommentsAPI(ListCreateAPIView):
    serializer_class = CommentSerializer
    filterset_fields = ['project', 'task', ]

    def get_queryset(self):
        user = self.request.user
        comments = Comment.objects.filter(project__users__in=user.projects.all())
        return comments

    def perform_create(self, serializer):
        user = self.request.user
        project = self.get_object()
        obj = serializer.save(owner=self.request.user, project=project)
        Activity(assignee=user, project=project, comment=obj, status='C',
                 description=f'{user} created a comment: {obj.project.title}').save()
        return obj


class ActivityAPI(ListAPIView):
    serializer_class = ActivitySerializer
    filterset_fields = {'assignee': ['exact'],
                        'project': ['exact'],
                        'section': ['exact'],
                        'task': ['exact'],
                        'comment': ['exact'],
                        'status': ['exact'],
                        'created': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def boolean(self, string):
        response = True
        if string == 0:
            response = False
        if string == 1:
            response = True
        if isinstance(string, basestring):
            if string.lower() in ["0", "no", "false"]:
                response = False
            if string.lower() in ["1", "yes", "true"]:
                response = True
        return response

    def get(self, request, *args, **kwargs):
        if not self.boolean(request.GET.get('pagination')):
            self.pagination_class = None
        if self.boolean(request.GET.get('lite')):
            self.serializer_class = ActivityLiteSerializer
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(project__users__in=user.projects.all())
