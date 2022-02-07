from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Team, MyUser


class TeamSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False, read_only=True)
    users = UserSerializer(read_only=True, required=False, many=True)

    class Meta:
        model = Team
        fields = '__all__'


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_img',
                  'header_img', 'timezone', 'setting']

