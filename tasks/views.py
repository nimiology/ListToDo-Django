from rest_framework.exceptions import AuthenticationFailed

from tasks.models import Project
from tasks.permissions import IsCreatorOrCreatOnly
from tasks.serializers import ProjectSerializer
from tasks.utils import CreateRetrieveUpdateDestroyAPIView


class ProjectsAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsCreatorOrCreatOnly]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(owner=self.request.user)
        else:
            raise AuthenticationFailed