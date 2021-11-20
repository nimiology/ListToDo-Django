from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

from tasks_api.utils import upload_file
from users.signals import team_pre_save


class Team(models.Model):
    name = models.CharField(max_length=250)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teams_owner')
    users = models.ManyToManyField(User, related_name='teams')
    profile = models.ImageField(upload_to=upload_file, blank=True)
    inviteSlug = models.SlugField(blank=True, null=True)


class Setting(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='setting')
    setting = models.JSONField()

    def __str__(self):
        return self.owner.username


pre_save.connect(team_pre_save, Team)
