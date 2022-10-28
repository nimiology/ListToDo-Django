from django.contrib.auth import get_user_model
from django.db import models

from project.models import Project
from task.models import Task
from task.utils import upload_file


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

