from rest_framework.permissions import BasePermission


class IsOwnerOrCreatOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.owner and request.user.is_authenticated) or request.method == 'POST'


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsInProjectOrCreatOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return ((request.user == obj.owner or request.user in obj.users.all())
                and request.user.is_authenticated) or request.method == 'POST'


class IsItUsersProjectWithProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.projects.all()


class IsItUsersProjectWithOBJ(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project in request.user.projects.all()
