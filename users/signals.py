def MyUser_pre_save(sender, instance, *args, **kwargs):
    print(instance.first_name)
    if not instance.first_name:
        instance.first_name = instance.username
