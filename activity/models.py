from django.contrib.auth import get_user_model
from django.db import models

from comment.models import Comment
from project.models import Project
from section.models import Section
from task.models import Task


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
