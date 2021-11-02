from djoser.serializers import UserSerializer
from rest_framework import serializers

from tasks_api.models import Project, Label, Color, Section


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
    owner = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Section
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['project'] = ProjectSerializer(read_only=True)
        return super(SectionSerializer, self).to_representation(instance)
