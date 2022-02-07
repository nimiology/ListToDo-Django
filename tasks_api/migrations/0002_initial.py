# Generated by Django 3.2.8 on 2022-02-07 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('tasks_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='tasks_api.Label'),
        ),
        migrations.AddField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks_api.section'),
        ),
        migrations.AddField(
            model_name='task',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='tasks_api.task'),
        ),
        migrations.AddField(
            model_name='section',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='tasks_api.project'),
        ),
        migrations.AddField(
            model_name='projectuser',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='projects', to='tasks_api.Label'),
        ),
        migrations.AddField(
            model_name='projectuser',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projectuser',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='tasks_api.project'),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subprojects', to='tasks_api.project'),
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='users.team'),
        ),
        migrations.AddField(
            model_name='label',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasks_api.project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasks_api.task'),
        ),
        migrations.AddField(
            model_name='activity',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity', to='tasks_api.comment'),
        ),
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='tasks_api.project'),
        ),
        migrations.AddField(
            model_name='activity',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity', to='tasks_api.section'),
        ),
        migrations.AddField(
            model_name='activity',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity', to='tasks_api.task'),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('section', 'position')},
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('project', 'position')},
        ),
        migrations.AlterUniqueTogether(
            name='projectuser',
            unique_together={('owner', 'position'), ('owner', 'project')},
        ),
    ]
