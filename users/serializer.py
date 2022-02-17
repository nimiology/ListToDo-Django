from rest_framework import serializers

from users.models import Team, MyUser


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_img',
                  'header_img', 'timezone', 'setting', 'date_joined']
        extra_kwargs = {'date_joined': {'read_only': True},
                        'username': {'required': False}}


class TeamSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(required=False, read_only=True)
    users = MyUserSerializer(read_only=True, required=False, many=True)

    class Meta:
        model = Team
        fields = '__all__'
