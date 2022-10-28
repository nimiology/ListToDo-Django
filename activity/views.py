from requests.compat import basestring
from rest_framework.generics import ListAPIView

from activity.models import Activity
from activity.serializers import ActivitySerializer, ActivityLiteSerializer


class ActivityAPI(ListAPIView):
    serializer_class = ActivitySerializer
    filterset_fields = {'assignee': ['exact'],
                        'project': ['exact'],
                        'section': ['exact'],
                        'task': ['exact'],
                        'comment': ['exact'],
                        'status': ['exact'],
                        'created': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def boolean(self, string):
        response = True
        if string == 0:
            response = False
        if string == 1:
            response = True
        if isinstance(string, basestring):
            if string.lower() in ["0", "no", "false"]:
                response = False
            if string.lower() in ["1", "yes", "true"]:
                response = True
        return response

    def get(self, request, *args, **kwargs):
        if not self.boolean(request.GET.get('pagination')):
            self.pagination_class = None
        if self.boolean(request.GET.get('lite')):
            self.serializer_class = ActivityLiteSerializer
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(project__users__in=user.projects.all())
