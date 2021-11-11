from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ReadOnlyField

from tasks_api.models import Project, Label, Color, Section, Task, Comment, Activity


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
    users = UserSerializer(read_only=True, many=True)


    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['position']
        read_only_fields = ('inviteSlug',)

    def to_representation(self, instance):
        self.fields['label'] = LabelSerializer(read_only=True, many=True)
        self.fields['position'] = PositionSerializer(read_only=True, many=True)

        return super(ProjectSerializer, self).to_representation(instance)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['project'] = ProjectSerializer(read_only=True)
        self.fields['position'] = PositionSerializer(read_only=True, many=True)
        return super(SectionSerializer, self).to_representation(instance)


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)
    section = SectionSerializer(read_only=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['assignee'] = UserSerializer(read_only=True)
        self.fields['task'] = ReadOnlyField(source='task.title')
        self.fields['color'] = ColorSerializer(read_only=True)
        self.fields['label'] = LabelSerializer(read_only=True)
        self.fields['position'] = PositionSerializer(read_only=True, many=True)
        return super(TaskSerializer, self).to_representation(instance)


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)
    project = ProjectSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        if 'file' in attrs:
            file_size = attrs['file'].size
            limit_mb = 10
            if file_size > limit_mb * 1024 * 1024:
                raise ValidationError({"file": ["The file must be less than 10MB"]})
        return attrs

    def to_representation(self, instance):
        self.fields['task'] = TaskSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['assignee'] = UserSerializer(read_only=True)
        self.fields['project'] = ProjectSerializer(read_only=True)
        self.fields['section'] = SectionSerializer(read_only=True)
        self.fields['task'] = TaskSerializer(read_only=True)
        self.fields['comment'] = CommentSerializer(read_only=True)
        return super(ActivitySerializer, self).to_representation(instance)


