from rest_framework.permissions import BasePermission

from project.models import ProjectUser


class IsOwnerOrCreatOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.method == 'POST'


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsInProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            obj.users.get(owner=request.user)
            return True
        except ProjectUser.DoesNotExist:
            return False


class IsItUsersProjectWithProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            obj.users.get(owner=request.user)
            return True
        except ProjectUser.DoesNotExist:
            return False


class IsItUsersProjectWithSection(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            obj.project.users.get(owner=request.user)
            return True
        except ProjectUser.DoesNotExist:
            return False


class IsItUsersProjectWithTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            obj.section.project.users.get(owner=request.user)
            return True
        except ProjectUser.DoesNotExist:
            return False
