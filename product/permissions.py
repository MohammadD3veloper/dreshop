from fcntl import F_SEAL_SHRINK
from django.http import Http404
from rest_framework import permissions



class IsSellerOrReadOnly(permissions.BasePermission): 
    def has_permission(self, request, view):
        if request.user.is_seller:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        raise Http404



class IsSupporterOrReadOnly(permissions.BasePermission): 
    def has_permission(self, request, view):
        if request.user.is_supporter:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        raise Http404



class IsSuperUserOrReadOnly(permissions.BasePermission): 
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        raise Http404


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_author:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        raise Http404



class IsSelfOrReadOnlyObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        raise Http404



class IsSelfOr404(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        else:
            raise Http404
