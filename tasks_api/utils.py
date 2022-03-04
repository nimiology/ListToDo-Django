import os
import random
import string

from requests.compat import basestring
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file(instance, filename):
    name, ext = get_filename_ext(filename)
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    final_name = f"{''.join(random.choice(letters) for _ in range(40))}{ext}"
    return f"{instance.owner.username}/{final_name}"


def slug_genrator():
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    SLUG = "".join(random.choice(letters) for _ in range(40))

    return SLUG


class CreateRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    pass


def check_task_in_project(serializer, project):
    task = serializer.validated_data.get('task')
    if task:
        if task.project != project:
            raise ValidationError("The task is not in the project!")

