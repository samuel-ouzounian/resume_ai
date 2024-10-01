from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUserOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff

class IsAdminUserForAllButCreate(BasePermission):
    """
    Custom permission to allow anyone to create, but only admin users for other actions.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.user and request.user.is_staff