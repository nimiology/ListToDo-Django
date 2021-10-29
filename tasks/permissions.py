from rest_framework.permissions import BasePermission


class IsCreatorOrCreatOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool((request.user == obj.owner and request.user.is_authenticated) or request.method == 'POST')
