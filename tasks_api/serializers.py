from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tasks_api.models import Project, Label, Section, Task, Comment, Activity, ProjectUser
from users.serializers import MyUserSerializer


class ProjectUsersSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)

    class Meta:
        model = ProjectUser
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)

    class Meta:
        model = Label
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('inviteSlug', 'inbox')

    def to_representation(self, instance):
        self.fields['users'] = ProjectUsersSerializer(read_only=True, many=True)
        self.fields['label'] = LabelSerializer(read_only=True, many=True)
        self.fields['parent_projects'] = ProjectSerializer(many=True)
        self.fields['count_subprojects'] = serializers.ReadOnlyField()
        self.fields['count_section'] = serializers.ReadOnlyField()
        self.fields['count_tasks'] = serializers.ReadOnlyField()
        return super(ProjectSerializer, self).to_representation(instance)


class ProjectUsersPersonalizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ['label', 'color', 'background']

    def to_representation(self, instance):
        self.fields['id'] = serializers.ReadOnlyField()
        self.fields['position'] = serializers.ReadOnlyField()
        self.fields['owner'] = MyUserSerializer(read_only=True)
        self.fields['project'] = ProjectSerializer(read_only=True)
        self.fields['label'] = LabelSerializer(read_only=True, many=True)
        return super(ProjectUsersPersonalizeSerializer, self).to_representation(instance)


class SectionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True, required=False)

    class Meta:
        model = Section
        fields = '__all__'
        extra_kwargs = {'position': {'required': False}}


class TaskSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)
    section = SectionSerializer(read_only=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {'position': {'required': False}}

    def to_representation(self, instance):
        self.fields['assignee'] = MyUserSerializer(read_only=True)
        self.fields['label'] = LabelSerializer(read_only=True, many=True)
        self.fields['parent_tasks'] = TaskSerializer(many=True)
        return super(TaskSerializer, self).to_representation(instance)


class CommentSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)
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
        self.fields['assignee'] = MyUserSerializer(read_only=True)
        self.fields['project'] = ProjectSerializer(read_only=True)
        self.fields['section'] = SectionSerializer(read_only=True)
        self.fields['task'] = TaskSerializer(read_only=True)
        self.fields['comment'] = CommentSerializer(read_only=True)
        return super(ActivitySerializer, self).to_representation(instance)


class ActivityLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'created']


class ProjectUsersSerializer4JoinProject(serializers.ModelSerializer):
    project = ProjectSerializer(required=False)
    owner = MyUserSerializer(read_only=True, required=False)

    class Meta:
        model = ProjectUser
        fields = '__all__'
        extra_kwargs = {'position': {'required': False}}


class ChangeProjectPositionSerializer(serializers.Serializer):
    obj = serializers.PrimaryKeyRelatedField(queryset=ProjectUser.objects.all())
    position = serializers.IntegerField()


class ChangeSectionPositionSerializer(serializers.Serializer):
    obj = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    position = serializers.IntegerField()


class ChangeTaskPositionSerializer(serializers.Serializer):
    obj = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    position = serializers.IntegerField()
