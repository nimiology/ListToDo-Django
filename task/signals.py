import datetime

from rest_framework.exceptions import ValidationError


def task_pre_save(sender, instance, *args, **kwargs):
    if instance.position is None:
        tasks = sender.objects.filter(section=instance.section).order_by('-position')
        if tasks.exists():
            instance.position = tasks[0].position + 1
        else:
            instance.position = 0
    if instance.completed:
        instance.completedDate = datetime.datetime.now()
        every = instance.every
        if every:
            today = datetime.date.today()
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
            if instance.schedule is None:
                instance.schedule = datetime.datetime.now()
            schedulestr = f"{day.strftime('%d-%b-%Y')} ({instance.schedule.strftime('%H:%M:%S.%f')})"
            schedule = datetime.datetime.strptime(schedulestr, '%d-%b-%Y (%H:%M:%S.%f)')
            new_task = sender.objects.create(
                owner=instance.owner, every=instance.every,
                assignee=instance.assignee, section=instance.section,
                task=instance.task, title=instance.title,
                description=instance.description, color=instance.color,
                priority=instance.priority, schedule=schedule,
                created=instance.created
            )
            new_task.label.set(instance.label.all())
    else:
        instance.completedDate = None
