from rest_framework import permissions

from .utils import is_in_group

class HasGroupPermission(permissions.BasePermission):
    """
    Ensure that user is in required groups.
    """
    def has_permission(self, request, view):    
        if request.user.is_superuser:
            return True
        else:
            required_groups_mapping = getattr(view, 'required_groups', {})
            required_groups = required_groups_mapping.get(request.method, [])
            return all([is_in_group(request.user, group_name) for group_name in required_groups])