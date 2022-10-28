from rest_framework.serializers import ModelSerializer

from activity.models import Activity
from comment.serializers import CommentSerializer
from project.serializers import ProjectSerializer
from section.serializers import SectionSerializer
from task.serializers import TaskSerializer
from users.serializers import MyUserSerializer


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['assignee'] = MyUserSerializer(read_only=True)
        self.fields['project'] = ProjectSerializer(read_only=True)
        self.fields['section'] = SectionSerializer(read_only=True)
        self.fields['task'] = TaskSerializer(read_only=True)
        self.fields['comment'] = CommentSerializer(read_only=True)
        return super(ActivitySerializer, self).to_representation(instance)


class ActivityLiteSerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'created']
