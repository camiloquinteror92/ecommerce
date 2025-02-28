# backend/shop/api/permissions.py
from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAdminOrManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'manager']
        )
