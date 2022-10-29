from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from label.serializers import LabelSerializer
from project.models import ProjectUser
from section.serializers import SectionSerializer
from task.models import Task
from task.utils import change_position
from users.serializers import MyUserSerializer


class TaskSerializer(ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)
    position = serializers.IntegerField(required=False, default=None)

    class Meta:
        model = Task
        fields = '__all__'

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def validate(self, attrs):
        assignee = attrs.get('assignee')
        section = attrs.get('section')
        task = attrs.get('task')
        labels = attrs.get('label')
        if labels:
            for label in labels:
                if label.owner != self._user():
                    raise ValidationError('The label is not found!')
        if section:
            project = section.project
        elif self.instance:
            project = self.instance.section.project
        else:
            return attrs
        if assignee:
            try:
                ProjectUser.objects.get(project=project, owner=assignee)
            except ProjectUser.DoesNotExist:
                raise ValidationError('The assignee is not in the project!')
        if task:
            if task.section.project != project:
                raise ValidationError('The task is not found!')

        return attrs

    def save(self, **kwargs):
        if self.instance is not None:
            position = self.validated_data.get('position')
            if position is not None:
                kwargs_for_function = {}
                section = self.validated_data.get('section')
                if section is not None:
                    kwargs_for_function['section'] = section
                else:
                    kwargs_for_function['section'] = self.instance.section
                change_position(instance_class=self.Meta.model, instance=self.instance, position=position,
                                **kwargs_for_function)
        return super(TaskSerializer, self).save(**kwargs)

    def to_representation(self, instance):
        self.fields['section'] = SectionSerializer(read_only=True, )
        self.fields['assignee'] = MyUserSerializer(read_only=True)
        self.fields['label'] = LabelSerializer(read_only=True, many=True)
        self.fields['parent_tasks'] = TaskSerializer(many=True)
        return super(TaskSerializer, self).to_representation(instance)
