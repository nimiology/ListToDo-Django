from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Setting, Team


class TeamSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False, read_only=True)
    users = UserSerializer(read_only=True, required=False, many=True)

    class Meta:
        model = Team
        fields = '__all__'


class SettingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Setting
        fields = '__all__'
