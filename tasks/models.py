from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, m2m_changed, pre_save
from rest_framework.exceptions import ValidationError

from tasks.utils import upload_file, slug_genrator


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
    user = models.ManyToManyField(User, blank=True, related_name=related_name)
    project = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subprojects')
    inviteSlug = models.SlugField(blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    label = models.ManyToManyField(Label, blank=True, related_name=related_name)
    background = models.ImageField(upload_to=upload_file, blank=True, null=True)
    view = models.CharField(max_length=1, default='L', choices=VIEWS_CHOICES)
    archive = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    schedule = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'

    class Meta:
        unique_together = [['owner', 'position']]


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

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_creator')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name=related_name)
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
        return f'{self.owner.username} - {self.title}'


class Comment(models.Model):
    related_name = 'comments'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=upload_file, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.username} - {self.pk}'


class Activity(models.Model):
    related_name = 'activity'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.username} - {self.pk}'


def ProjectPreSave(sender, instance, *args, **kwargs):
    if instance.inviteSlug == '':
        instance.inviteSlug = slug_genrator(Project)
    if not instance.position:
        qs = Project.objects.filter(owner=instance.owner).order_by('-id')
        if qs.exists():
            instance.position = qs[0].position + 1
        else:
            instance.position = 1


def LabelProjectM2MChanged(sender, instance, *args, **kwargs):
    if 'post' in kwargs['action']:
        for label in instance.label.all():
            if label.owner != instance.owner:
                raise ValidationError('Invalid Label')


# def ProjectUserM2MChanged(sender, instance, *args, **kwargs):
#     if 'post' in kwargs['action']:
#         if instance.owner not in instance.user.all():
#             instance.user.add(instance.owner)
#
#
# m2m_changed.connect(ProjectUserM2MChanged, Project.user.through)
m2m_changed.connect(LabelProjectM2MChanged, Project.label.through)
pre_save.connect(ProjectPreSave, Project)
