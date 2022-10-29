# Generated by Django 3.2.8 on 2022-10-28 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('section', '0001_initial'),
        ('activity', '0002_activity_comment'),
        ('project', '0001_initial'),
        ('task', '0005_auto_20221028_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='project.project'),
        ),
        migrations.AddField(
            model_name='activity',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity', to='section.section'),
        ),
        migrations.AddField(
            model_name='activity',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity', to='task.task'),
        ),
    ]