import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model

from config import settings
from task.utils import upload_file
from users.signals import MyUser_pre_save


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
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='teams_owner')
    users = models.ManyToManyField(get_user_model(), blank=True, related_name='teams')
    profile = models.ImageField(upload_to=upload_file, blank=True)
    inviteSlug = models.SlugField(blank=True, null=True)


pre_save.connect(MyUser_pre_save, MyUser)
