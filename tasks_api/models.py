from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed, pre_save, post_save

from tasks_api.signals import label_project_m2m_changed, project_pre_save, task_pre_save
from tasks_api.utils import upload_file


class Color(models.Model):
    title = models.CharField(primary_key=True, max_length=256)

    def __str__(self):
        return self.title


class Label(models.Model):
    related_name = 'labels'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_owner')
    users = models.ManyToManyField(User, blank=True, related_name=related_name)
    project = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subprojects')
    inviteSlug = models.SlugField(blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    label = models.ManyToManyField(Label, blank=True, related_name=related_name)
    background = models.ImageField(upload_to=upload_file, blank=True, null=True)
    archive = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    schedule = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'


class Section(models.Model):
    title = models.CharField(max_length=512)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name='sections')
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.project} - {self.title}'


class Task(models.Model):
    related_name = 'tasks'
    PRIORITY_CHOICES = (
        ('1', 'Priority 1'),
        ('2', 'Priority 2'),
        ('3', 'Priority 3'),
        ('4', 'Priority 4'),
        ('5', 'Priority 5'),
    )
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

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_creator')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name=related_name)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name=related_name)
    task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, blank=True, null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    schedule = models.DateTimeField(blank=True, null=True)
    every = models.CharField(max_length=1, choices=EVERYDAY_STATUS, blank=True, null=True)
    completedDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'


class Comment(models.Model):
    related_name = 'comments'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
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

    assignee = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name=related_name)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name=related_name)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.project} - {self.pk}'


def user_post_save(sender, instance, *args, **kwargs):
    if kwargs['created']:
        Project(title='inbox', owner=instance).save()


m2m_changed.connect(label_project_m2m_changed, Project.label.through)
pre_save.connect(project_pre_save, Project)
pre_save.connect(task_pre_save, Task)
post_save.connect(user_post_save, User)
