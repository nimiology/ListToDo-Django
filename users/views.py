import pytz
from django.db.models import Q
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks_api.models import ProjectUser
from tasks_api.permissions import IsOwnerOrCreatOnly
from tasks_api.utils import CreateRetrieveUpdateDestroyAPIView
from tasks_api.views import ChangeInviteSlugProject
from users.models import Team, MyUser
from users.permissions import IsInTeam, ReadOnly, IsTeamOwner
from users.serializers import MyUserSerializer, TeamSerializer


class TeamAPI(CreateRetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    permission_classes = [IsOwnerOrCreatOnly | (IsInTeam & ReadOnly)]
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(owner=self.request.user)


class JoinTeamAPI(RetrieveAPIView):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    lookup_field = 'inviteSlug'

    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):
        team = self.get_object()
        user = request.user
        if team.owner != user:
            team.users.add(user)
            for project in team.projects.all():
                ProjectUser(owner=user, project=project).save()
            return self.retrieve(request, *args, **kwargs)
        else:
            raise ValidationError("You can't join to your own team!")


class LeaveTeamAPI(RetrieveAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsInTeam]
    queryset = Team.objects.all()

    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def post(self, request, *args, **kwargs):
        team = self.get_object()
        if team.owner != request.user:
            team.users.remove(request.user)
            serializer = self.get_serializer(team)
            return Response(serializer.data)

        else:
            raise ValidationError("You can't leave to your own team!")


class AllTeamsAPI(ListAPIView):
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.filter(Q(owner=self.request.user) | Q(users__in=[self.request.user]))


class ChangeInviteSlugTeam(ChangeInviteSlugProject):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsTeamOwner]
    queryset = Team.objects.all()


class MyUsersAPI(RetrieveUpdateAPIView):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    permission_classes = [IsOwnerOrCreatOnly]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        return serializer.save(owner=self.request.user)


timezones = [{'id': str(number), 'timezone': pytz.all_timezones[number]} for number in
             range(0, len(pytz.all_timezones))]


class GetAllTimeZonesAPI(APIView):
    def get(self, request, *args, **kwargs):
        return Response(timezones)
