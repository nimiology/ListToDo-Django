from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Setting


class SettingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Setting
        fields = '__all__'

