from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import m2m_changed, pre_save, post_save

from tasks_api.signals import label_project_m2m_changed, project_pre_save, task_pre_save, project_users_pre_save, \
    section_pre_save
from tasks_api.utils import upload_file
from users.models import Team, MyUser

COLORS_CHOICES = [[str(i), str(i)] for i in range(1, 9)]


class Label(models.Model):
    related_name = 'labels'

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=related_name)
    title = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'


class Project(models.Model):
    related_name = 'projects'
    VIEWS_CHOICES = [
        ('L', 'List'),
        ('B', 'Board'),
    ]
    title = models.CharField(max_length=512)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='projects_owner')
    project = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subprojects')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    inviteSlug = models.SlugField(blank=True, null=True)
    archive = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    schedule = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'

    def parent_projects(self):
        project = self.project
        projects = []
        while project:
            projects.append(project.pk)
            project = project.project
        return projects


class ProjectUser(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='users')
    position = models.IntegerField(blank=True, null=True)
    label = models.ManyToManyField(Label, blank=True, related_name='projects')
    color = models.CharField(max_length=1, choices=COLORS_CHOICES, null=True, blank=True)
    background = models.ImageField(upload_to=upload_file, blank=True, null=True)

    def __str__(self):
        return f'{self.owner} - {self.project}'

    class Meta:
        unique_together = [['owner', 'project'], ['owner', 'position']]


class Section(models.Model):
    title = models.CharField(max_length=512)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sections')
    position = models.IntegerField(blank=True, null=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.project} - {self.title}'

    class Meta:
        unique_together = ['project', 'position']
        ordering = ['position']


class Task(models.Model):
    related_name = 'tasks'
    PRIORITY_CHOICES = [[str(i), f'Priority {i}'] for i in range(1, 6)]

    EVERYDAY_STATUS = (
        ('0', 'EveryDay'),
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday'),
    )

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='task_creator')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name=related_name)
    assignee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True,
                                 related_name=related_name)
    task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=1, choices=COLORS_CHOICES, null=True, blank=True)
    label = models.ManyToManyField(Label, blank=True, related_name=related_name)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    schedule = models.DateTimeField(blank=True, null=True)
    every = models.CharField(max_length=1, choices=EVERYDAY_STATUS, blank=True, null=True)
    completedDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'

    class Meta:
        unique_together = ['section', 'position']
        ordering = ['position']

    def parent_tasks(self):
        task = self.task
        tasks = []
        while task:
            tasks.append(task.pk)
            task = task.task
        return tasks


class Comment(models.Model):
    related_name = 'comments'

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=related_name)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name=related_name)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    description = models.TextField()
    file = models.FileField(upload_to=upload_file, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.owner.username} - {self.pk}'


class Activity(models.Model):
    related_name = 'activity'
    STATUS_CHOICES = (
        ('C', 'Created'),
        ('U', 'Updated'),
        ('D', 'Deleted')
    )

    assignee = models.ForeignKey(get_user_model(), models.SET_NULL, null=True, blank=True, related_name=related_name)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name=related_name)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.project} - {self.pk}'


def user_post_save(sender, instance, created, *args, **kwargs):
    if created:
        Project(title='inbox', owner=instance).save()


def project_post_save(sender, instance, created, *args, **kwargs):
    if created:
        ProjectUser(owner=instance.owner, project=instance).save()

        if instance.team:
            if instance.owner != instance.team.owner:
                ProjectUser(owner=instance.team.owner, project=instance).save()
            for user in instance.team.users.all():
                if instance.owner != user:
                    ProjectUser(owner=user, project=instance).save()


m2m_changed.connect(label_project_m2m_changed, ProjectUser.label.through)
pre_save.connect(project_pre_save, Project)
pre_save.connect(project_users_pre_save, ProjectUser)
pre_save.connect(task_pre_save, Task)
pre_save.connect(section_pre_save, Section)
post_save.connect(user_post_save, get_user_model)
post_save.connect(project_post_save, Project)


def MyUser_post_save(sender, created, instance, *args, **kwargs):
    if created:
        Project.objects.create(owner=instance, title='inbox')


post_save.connect(MyUser_post_save, MyUser)
