from rest_framework import permissions
from .models import User


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user and request.user.is_authenticated:
            if (request.user.is_teacher):
                return True
        return False


class IsTeacherOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            if view.action == 'create':
                if (request.user.is_teacher):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if not (request.user.is_teacher):
                return True
        return False

class IsNotMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if not (request.user.is_mentor):
                return True
        return False


class IsMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if (request.user.is_mentor):
                return True
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user
