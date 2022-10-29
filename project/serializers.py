from rest_framework import serializers

from label.serializers import LabelSerializer
from project.models import ProjectUser, Project
from task.utils import change_position
from users.serializers import MyUserSerializer


class ProjectUsersSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)

    class Meta:
        model = ProjectUser
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
        fields = ['label', 'color', 'background', 'position']

    def save(self, **kwargs):
        if self.instance is not None:
            position = self.validated_data.get('position')
            if position is not None:
                change_position(instance_class=self.Meta.model, instance=self.instance, position=position,
                                owner=self.instance.owner)
        return super(ProjectUsersPersonalizeSerializer, self).save(**kwargs)

    def to_representation(self, instance):
        self.fields['id'] = serializers.ReadOnlyField()
        self.fields['owner'] = MyUserSerializer(read_only=True)
        self.fields['project'] = ProjectSerializer(read_only=True)
        self.fields['label'] = LabelSerializer(read_only=True, many=True)
        return super(ProjectUsersPersonalizeSerializer, self).to_representation(instance)


class ProjectUsersSerializer4JoinProject(serializers.ModelSerializer):
    project = ProjectSerializer(required=False)
    owner = MyUserSerializer(read_only=True, required=False)

    class Meta:
        model = ProjectUser
        fields = '__all__'
