from rest_framework.exceptions import ValidationError

from task.utils import slug_generator


def project_pre_save(sender, instance, *args, **kwargs):
    if not instance.invite_slug:
        instance.invite_slug = slug_generator()

    if instance.project:
        if instance.project.owner != instance.owner:
            raise ValidationError("That's not your project!")

        if instance.project == instance:
            instance.project = None

        if instance.project.project == instance:
            raise ValidationError("most likely due to a circular parent projects")
    else:
        try:
            inbox_project = sender.objects.get(owner=instance.owner, inbox=True)
            instance.project = inbox_project
        except sender.DoesNotExist:
            pass

    if instance.team:
        if not instance.team.owner == instance.owner and not instance.owner in instance.team.users.all():
            raise ValidationError("You're not in the team!")

    if instance.inbox:
        if instance.pk:
            raise ValidationError("Can't modify inbox")


def project_users_pre_save(sender, instance, *args, **kwargs):
    if instance.position is None:
        projects_user = sender.objects.filter(owner=instance.owner).order_by('-position')
        if projects_user.exists():
            if len(projects_user) > 1:
                project_user = projects_user[0]
                instance.position = project_user.position + 1
            else:
                instance.position = 1
        else:
            instance.position = 0


def label_project_m2m_changed(sender, instance, *args, **kwargs):
    if 'post' in kwargs['action']:
        for label in instance.label.all():
            if label.owner != instance.owner:
                raise ValidationError('Invalid Label')

