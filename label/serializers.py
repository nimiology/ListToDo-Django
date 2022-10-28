from rest_framework.serializers import ModelSerializer

from label.models import Label
from users.serializers import MyUserSerializer


class LabelSerializer(ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)

    class Meta:
        model = Label
        fields = '__all__'
