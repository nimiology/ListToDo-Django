from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from label.models import Label
from label.serializers import LabelSerializer
from task.permissions import IsOwnerOrCreatOnly


class LabelAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    permission_classes = [IsOwnerOrCreatOnly]
    queryset = Label.objects.all()

    def perform_update(self, serializer):
        return serializer.save(owner=self.get_object().owner)


class MyLabelListCreateAPI(ListCreateAPIView):
    serializer_class = LabelSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user)
