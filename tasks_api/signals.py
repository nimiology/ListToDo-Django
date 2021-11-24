import datetime

from rest_framework.exceptions import ValidationError

from tasks_api.utils import slug_genrator


def project_pre_save(sender, instance, *args, **kwargs):
    if not instance.inviteSlug:
        instance.inviteSlug = slug_genrator()

    if instance.project:
        if instance.project.owner != instance.owner:
            raise ValidationError("That's not your project!")

    if instance.team:
        if not instance.team.owner == instance.owner and not instance.owner in instance.team.users.all():
            raise ValidationError("You're not in the team!")


def section_pre_save(sender, instance, *args, **kwargs):
    if instance.position is None:
        project_sections = sender.objects.filter(project=instance.project).order_by('-position')
        if project_sections.exists():
            project_section = project_sections[0]
            instance.position = project_section.position + 1
        else:
            instance.position = 0


def project_users_pre_save(sender, instance, *args, **kwargs):
    if instance.position is None:
        projects_user = sender.objects.filter(owner=instance.owner).order_by('-position')
        if projects_user.exists():
            project_user = projects_user[0]
            instance.position = project_user.position + 1
        else:
            instance.position = -1


def task_pre_save(sender, instance, *args, **kwargs):
    if instance.position is None:
        tasks = sender.objects.filter(section=instance.section).order_by('-position')
        if tasks.exists():
            last_task = tasks[0]
            instance.position = last_task.position + 1
        else:
            instance.position = 0
    if instance.completed:
        instance.completedDate = datetime.datetime.now()
        every = instance.every
        if every:
            today = datetime.date.today()
            instance.schedule.strftime("%d-%b-%Y (%H:%M:%S.%f)")

            if every == '0':
                day = datetime.datetime.now() + datetime.timedelta(days=1)
            elif every == '1':
                day = today + datetime.timedelta(days=(6 - today.weekday()) % 7)
            elif every == '2':
                day = today + datetime.timedelta(days=(0 - today.weekday()) % 7)
            elif every == '3':
                day = today + datetime.timedelta(days=(1 - today.weekday()) % 7)
            elif every == '4':
                day = today + datetime.timedelta(days=(2 - today.weekday()) % 7)
            elif every == '5':
                day = today + datetime.timedelta(days=(3 - today.weekday()) % 7)
            elif every == '6':
                day = today + datetime.timedelta(days=(4 - today.weekday()) % 7)
            elif every == '7':
                day = today + datetime.timedelta(days=(5 - today.weekday()) % 7)
            else:
                raise ValidationError('WTF!')
            if day.day == today.day:
                day = today + datetime.timedelta(days=7)
            schedulestr = f"{day.strftime('%d-%b-%Y')} ({instance.schedule.strftime('%H:%M:%S.%f')})"
            schedule = datetime.datetime.strptime(schedulestr, '%d-%b-%Y (%H:%M:%S.%f)')
            sender(owner=instance.owner, project=instance.project,
                   assignee=instance.assignee, section=instance.section,
                   task=instance.task, title=instance.title,
                   description=instance.description, color=instance.color,
                   label=instance.label, priority=instance.priority,
                   position=instance.position, created=instance.created,
                   schedule=schedule,
                   every=instance.every).save()
    else:
        instance.completedDate = None


def label_project_m2m_changed(sender, instance, *args, **kwargs):
    if 'post' in kwargs['action']:
        for label in instance.label.all():
            if label.owner != instance.owner:
                raise ValidationError('Invalid Label')
