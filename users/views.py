from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from tasks_api.permissions import IsOwnerOrCreatOnly
from tasks_api.utils import CreateRetrieveUpdateDestroyAPIView
from users.models import Setting
from users.serializer import SettingSerializer


class SettingAPI(CreateRetrieveUpdateDestroyAPIView):
    serializer_class = SettingSerializer
    queryset = Setting.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrCreatOnly]

    def get_object(self):
        setting = get_object_or_404(self.get_queryset(), owner=self.request.user)
        return setting

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(owner=self.request.user)
