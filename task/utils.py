import os
import random
import string


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file(instance, filename):
    name, ext = get_filename_ext(filename)
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    final_name = f"{''.join(random.choice(letters) for _ in range(40))}{ext}"
    return final_name


def slug_generator():
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    return "".join(random.choice(letters) for _ in range(40))


def change_position(instance_class, instance, position, **kwargs):
    last_position_qs = instance_class.objects.filter(**kwargs).order_by('-position')
    if last_position_qs.exists():
        instance.position = last_position_qs[0].position + 10
        instance.save()

        instances_with_greater_positions = instance_class.objects.filter(position__gte=position, **kwargs).order_by('-position')

        for instance_with_greater_position in instances_with_greater_positions:
            if instance_with_greater_position != instance:
                instance_with_greater_position.position += 1
                instance_with_greater_position.save()
    instance.position = position
    instance.save()
