from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import Serializer, ModelSerializer

from project.serializers import ProjectSerializer
from section.models import Section
from task.utils import change_position


class SectionSerializer(ModelSerializer):
    position = IntegerField(required=False, default=None)

    class Meta:
        model = Section
        fields = '__all__'

    def save(self, **kwargs):
        if self.instance is not None:
            position = self.validated_data.get('position')
            if position is not None:
                kwargs_for_function = {}
                project = self.validated_data.get('project')
                if project is not None:
                    kwargs_for_function['project'] = project
                else:
                    kwargs_for_function['project'] = self.instance.project
                change_position(instance_class=self.Meta.model, instance=self.instance, position=position,
                                **kwargs_for_function)
        return super(SectionSerializer, self).save(**kwargs)

    def to_representation(self, instance):
        self.fields['project'] = ProjectSerializer(read_only=True)
        return super(SectionSerializer, self).to_representation(instance)
