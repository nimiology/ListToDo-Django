def MyUser_pre_save(sender, instance, *args, **kwargs):
    if not instance.first_name:
        instance.first_name = instance.username
