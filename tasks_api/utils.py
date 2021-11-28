import os
import random
import string

from rest_framework.exceptions import ValidationError, AuthenticationFailed
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


def check_creating_task(serializer, project, user):
    assignee = serializer.validated_data.get('assignee')
    section = serializer.validated_data.get('section')
    task = serializer.validated_data.get('task')
    label = serializer.validated_data.get('label')
    if assignee:
        if not assignee in project.users.all() and assignee != project.owner:
            raise ValidationError('The assignee is not in the project!')
    if section:
        if section.project != project:
            raise ValidationError('The section is not in the project!')
    if task:
        if task.project != project:
            raise ValidationError('The task is not found!')
    if label:
        for l in label:
            if l.owner != user:
                raise ValidationError('The label is not found!')


def check_task_in_project(serializer, project):
    task = serializer.validated_data.get('task')
    if task:
        if task.project != project:
            raise ValidationError("The task is not in the project!")

