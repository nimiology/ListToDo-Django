from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from comment.models import Comment
from project.models import ProjectUser
from project.serializers import ProjectSerializer
from task.serializers import TaskSerializer
from users.serializers import MyUserSerializer


class CommentSerializer(ModelSerializer):
    owner = MyUserSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = '__all__'

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def validate(self, attrs):
        if 'file' in attrs:
            file_size = attrs['file'].size
            limit_mb = 10
            if file_size > limit_mb * 1024 * 1024:
                raise ValidationError({"file": ["The file must be less than 10MB"]})
        task = attrs.get('task')
        if task:
            try:
                task.section.project.users.get(owner=self._user())
            except ProjectUser.DoesNotExist:
                raise ValidationError("The task is not in the project!")
        return attrs

    def to_representation(self, instance):
        self.fields['task'] = TaskSerializer(read_only=True)
        self.fields['project'] = ProjectSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)



