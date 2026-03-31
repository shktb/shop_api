from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class CanEditWithin15Minutes(BasePermission):
    def has_object_permission(self, request, view, obj):
        time_passed = timezone.now() - obj.created_at
        return time_passed <= timedelta(minutes=30)
    
class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return not(request.user and request.user.is_authenticated and request.user.is_staff)
        return request.user and request.user.is_authenticated and request.user.is_staff
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff