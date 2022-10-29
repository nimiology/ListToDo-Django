from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from label.models import Label
from section.models import Section
from task.signals import task_pre_save

from users.models import Team, MyUser


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
    COLORS_CHOICES = [[str(i), str(i)] for i in range(1, 9)]

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
        ordering = ['position']

    def parent_tasks(self):
        task = self.task
        tasks = []
        while task:
            tasks.append(task)
            task = task.task
        return tasks


pre_save.connect(task_pre_save, Task)
