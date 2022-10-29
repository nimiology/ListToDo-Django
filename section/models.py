from django.db import models
from django.db.models.signals import pre_save

from project.models import Project
from section.signals import section_pre_save


class Section(models.Model):
    title = models.CharField(max_length=512)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sections')
    position = models.IntegerField(blank=True, null=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.project} - {self.title}'

    class Meta:
        ordering = ['position']


pre_save.connect(section_pre_save, Section)
