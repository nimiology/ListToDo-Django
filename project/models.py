from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import m2m_changed, pre_save, post_save

from label.models import Label
from project.signals import project_users_pre_save, project_pre_save, label_project_m2m_changed
from task.utils import upload_file
from users.models import Team

COLORS_CHOICES = [[str(i), str(i)] for i in range(1, 9)]


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
    invite_slug = models.SlugField(blank=True, null=True)
    archive = models.BooleanField(default=False)
    inbox = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    schedule = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'

    def parent_projects(self):
        project = self.project
        projects = []
        while project:
            projects.append(project)
            project = project.project
        return projects

    def count_subprojects(self):
        return self.subprojects.count()

    def count_section(self):
        return self.sections.count()

    def count_tasks(self):
        number = 0
        sections = self.sections.all()
        for section in sections:
            number += section.tasks.count()
        return number


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


def project_post_save(sender, instance, created, *args, **kwargs):
    if created:
        ProjectUser.objects.create(owner=instance.owner, project=instance)

        if instance.team:
            if instance.owner != instance.team.owner:
                ProjectUser.objects.create(owner=instance.team.owner, project=instance)
            for user in instance.team.users.all():
                if instance.owner != user:
                    ProjectUser.objects.create(owner=user, project=instance)


def MyUser_post_save(sender, created, instance, *args, **kwargs):
    if created:
        Project.objects.create(owner=instance, title='inbox', inbox=True)


post_save.connect(MyUser_post_save, get_user_model())
m2m_changed.connect(label_project_m2m_changed, ProjectUser.label.through)
pre_save.connect(project_pre_save, Project)
pre_save.connect(project_users_pre_save, ProjectUser)
post_save.connect(project_post_save, Project)
