# Generated by Django 3.2.8 on 2021-10-29 09:37

from django.db import migrations, models
import tasks.utils


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_assignee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='owner',
            new_name='creator',
        ),
        migrations.AddField(
            model_name='project',
            name='background',
            field=models.ImageField(default='', upload_to=tasks.utils.upload_file),
            preserve_default=False,
        ),
    ]
