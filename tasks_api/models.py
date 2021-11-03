import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed, pre_save
from rest_framework.exceptions import ValidationError

from tasks_api.utils import upload_file, slug_genrator


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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name='sections')
    position = models.PositiveIntegerField(default=0)
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name=related_name)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name=related_name)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
    task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True, related_name=related_name)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, blank=True, null=True)
    position = models.PositiveIntegerField(default=0)
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


# class Activity(models.Model):
#     related_name = 'activity'
#     STATUS_CHOICES = (
#         ('C', 'Created'),
#         ('U', 'Updated'),
#         ('D', 'Deleted')
#     )
#
#     assignee = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, related_name=related_name)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name=related_name)
#     section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name=related_name)
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES)
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#
#     def __str__(self):
#         return f'{self.project} - {self.pk}'


def ProjectPreSave(sender, instance, *args, **kwargs):
    if instance.inviteSlug == '':
        instance.inviteSlug = slug_genrator(sender)

    if not instance.position:
        qs = sender.objects.filter(owner=instance.owner).order_by('-id')
        if qs.exists():
            instance.position = qs[0].position + 1
        else:
            instance.position = 1


def SectionPreSave(sender, instance, *args, **kwargs):
    if not instance.position:
        qs = sender.objects.filter(project=instance.project).order_by('-id')
        if qs.exists():
            instance.position = qs[0].position + 1
        else:
            instance.position = 1


def TaskPreSave(sender, instance, *args, **kwargs):
    if instance.completed:
        instance.completedDate = datetime.datetime.now()
        every = instance.every
        if every:
            today = datetime.date.today()
            instance.schedule.strftime("%d-%b-%Y (%H:%M:%S.%f)")

            if every == '0':
                day = datetime.datetime.now() + datetime.timedelta(days=1)
            elif every == '1':
                day = today + datetime.timedelta(days=(6 - today.weekday()) % 7)
            elif every == '2':
                day = today + datetime.timedelta(days=(0 - today.weekday()) % 7)
            elif every == '3':
                day = today + datetime.timedelta(days=(1 - today.weekday()) % 7)
            elif every == '4':
                day = today + datetime.timedelta(days=(2 - today.weekday()) % 7)
            elif every == '5':
                day = today + datetime.timedelta(days=(3 - today.weekday()) % 7)
            elif every == '6':
                day = today + datetime.timedelta(days=(4 - today.weekday()) % 7)
            elif every == '7':
                day = today + datetime.timedelta(days=(5 - today.weekday()) % 7)
            else:
                raise ValidationError('WTF!')
            if day.day == today.day:
                day = today + datetime.timedelta(days=7)
            schedulestr = f"{day.strftime('%d-%b-%Y')} ({instance.schedule.strftime('%H:%M:%S.%f')})"
            schedule = datetime.datetime.strptime(schedulestr, '%d-%b-%Y (%H:%M:%S.%f)')
            sender(owner=instance.owner, project=instance.project,
                   assignee=instance.assignee, section=instance.section,
                   task=instance.task, title=instance.title,
                   description=instance.description, color=instance.color,
                   label=instance.label, priority=instance.priority,
                   position=instance.position, created=instance.created,
                   schedule=schedule,
                   every=instance.every).save()
    else:
        instance.completedDate = None

    if not instance.position:
        qs = sender.objects.filter(section=instance.section).order_by('-id')
        if qs.exists():
            instance.position = qs[0].position + 1
        else:
            instance.position = 1


def LabelProjectM2MChanged(sender, instance, *args, **kwargs):
    if 'post' in kwargs['action']:
        for label in instance.label.all():
            if label.owner != instance.owner:
                raise ValidationError('Invalid Label')


m2m_changed.connect(LabelProjectM2MChanged, Project.label.through)
pre_save.connect(ProjectPreSave, Project)
pre_save.connect(SectionPreSave, Section)
pre_save.connect(TaskPreSave, Task)
