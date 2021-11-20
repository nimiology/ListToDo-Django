from tasks_api.utils import slug_genrator


def team_pre_save(sender, instance, *args, **kwargs):
    if not instance.inviteSlug:
        instance.inviteSlug = slug_genrator()
