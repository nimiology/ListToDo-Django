import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings
from tasks_api.utils import upload_file


class MyUser(AbstractUser):
    profile_img = models.ImageField(upload_to=upload_file, default='profile.jpg')
    header_img = models.ImageField(upload_to=upload_file, default='header.jpg')
    timezone = models.CharField(max_length=3,
                                choices=[(str(number), pytz.all_timezones[number]) for number in
                                         range(0, len(pytz.all_timezones))],
                                default=str(pytz.all_timezones.index(settings.TIME_ZONE)))
    setting = models.JSONField(null=True, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Team(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='teams_owner')
    users = models.ManyToManyField(MyUser, blank=True, related_name='teams')
    profile = models.ImageField(upload_to=upload_file, blank=True)
    inviteSlug = models.SlugField(blank=True, null=True)
