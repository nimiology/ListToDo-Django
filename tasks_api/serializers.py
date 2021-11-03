from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.serializers import ReadOnlyField

from tasks_api.models import Project, Label, Color, Section, Task, Comment


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Label
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['users'] = UserSerializer(read_only=True, many=True)
        self.fields['label'] = LabelSerializer(read_only=True, many=True)
        return super(ProjectSerializer, self).to_representation(instance)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['project'] = ProjectSerializer(read_only=True)
        return super(SectionSerializer, self).to_representation(instance)


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)
    project = ProjectSerializer(read_only=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['assignee'] = UserSerializer(read_only=True)
        self.fields['section'] = SectionSerializer(read_only=True)
        self.fields['task'] = ReadOnlyField(source='task.title')
        self.fields['color'] = ColorSerializer(read_only=True)
        self.fields['label'] = LabelSerializer(read_only=True)
        return super(TaskSerializer, self).to_representation(instance)


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)
    project = ProjectSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['task'] = TaskSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)