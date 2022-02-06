import pytz
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

from config import settings
from tasks_api.utils import upload_file
from users.signals import team_pre_save


class Team(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams_owner')
    users = models.ManyToManyField(User, blank=True, related_name='teams')
    profile = models.ImageField(upload_to=upload_file, blank=True)
    inviteSlug = models.SlugField(blank=True, null=True)


class Setting(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='setting')
    profile = models.ImageField(upload_to=upload_file, default='profile.jpg')
    header = models.ImageField(upload_to=upload_file, default='header.jpg')
    timezone = models.CharField(max_length=3,
                                choices=[(str(number), pytz.all_timezones[number]) for number in range(0, len(pytz.all_timezones))],
                                default=str(pytz.all_timezones.index(settings.TIME_ZONE)))
    setting = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.owner.username


pre_save.connect(team_pre_save, Team)
