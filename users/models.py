from django.contrib.auth.models import User
from django.db import models


class Setting(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='setting')
    setting = models.JSONField()

    def __str__(self):
        return self.owner.username
