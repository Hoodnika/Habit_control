from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'Its not your, bro'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMe(BasePermission):
    message = 'Это не твой профиль, ты куда лезешь'

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdmin(BasePermission):
    message = 'Ошибка в правах доступа'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin').exists()
