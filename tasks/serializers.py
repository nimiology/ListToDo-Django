from djoser.serializers import UserSerializer
from rest_framework import serializers

from tasks.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True, many=True)
        return super(ProjectSerializer, self).to_representation(instance)
