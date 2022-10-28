from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import Serializer, ModelSerializer

from project.serializers import ProjectSerializer
from section.models import Section


class SectionSerializer(ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['project'] = ProjectSerializer(read_only=True)
        return super(SectionSerializer, self).to_representation(instance)


class ChangeSectionPositionSerializer(Serializer):
    obj = PrimaryKeyRelatedField(queryset=Section.objects.all())
    position = IntegerField()
