# Generated by Django 3.2.8 on 2022-03-13 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_api', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='inbox',
            field=models.BooleanField(default=False),
        ),
    ]
