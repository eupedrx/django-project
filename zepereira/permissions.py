from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """
    Permission para permitir acesso apenas a usuários staff/admin.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
