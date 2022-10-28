from django.contrib.auth import get_user_model
from django.db import models


class Label(models.Model):
    related_name = 'labels'

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=related_name)
    title = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.owner.username} - {self.title}'
