# Generated by Django 3.2.8 on 2021-10-29 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_project_background'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='creator',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='creator',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='label',
            old_name='creator',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='creator',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='creator',
            new_name='owner',
        ),
    ]
