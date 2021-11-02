from rest_framework.permissions import BasePermission


class IsOwnerOrCreatOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.owner and request.user.is_authenticated) or request.method == 'POST'


class IsItOwnerOrUsersProjectWithProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all() or request.user == obj.owner


class IsItOwnerOrUsersProjectWithSection(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.project.users.all() or request.user == obj.project.owner
