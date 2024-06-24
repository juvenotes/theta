from rest_framework.permissions import BasePermission

class IsManagerOrContributor(BasePermission):
    """
    Allows access only to Manager or Contributor users.
    """
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_manager or request.user.is_contributor))

class IsManager(BasePermission):
    """
    Allows access only to Manager users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_manager)