from django.contrib.auth.models import User
from django.db import models

from tasks.utils import upload_file


class Color(models.Model):
    title = models.CharField(primary_key=True, max_length=256)

    def __str__(self):
        return self.title


class Label(models.Model):
    related_name = 'labels'

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
    title = models.CharField(primary_key=True, max_length=256)

    def __str__(self):
        return self.title


class Project(models.Model):
    related_name = 'projects'

    VIEWS_CHOICES = [
        ('L', 'List'),
        ('B', 'Board'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_owner')
    user = models.ManyToManyField(User, related_name=related_name)
    title = models.CharField(max_length=512)
    project = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subprojects')
    color = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    view = models.CharField(max_length=1, default='L', choices=VIEWS_CHOICES)
    archive = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    schedule = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'


class Section(models.Model):
    title = models.CharField(max_length=512)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name='section')
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.project} - {self.title}'


class Task(models.Model):
    related_name = 'tasks'
    PRIORITY_CHOICES = [
        ('1', 'Priority 1'),
        ('2', 'Priority 2'),
        ('3', 'Priority 3'),
        ('4', 'Priority 4'),
        ('5', 'Priority 5'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_creator')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, blank=True, null=True)
    position = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    schedule = models.DateTimeField(blank=True, null=True)
    complete = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.creator.username} - {self.title}'


class Comment(models.Model):
    related_name = 'comments'

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=upload_file, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.creator.username} - {self.task.title}'


class Activity(models.Model):
    related_name = 'activity'

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.creator.username} - {self.pk}'
