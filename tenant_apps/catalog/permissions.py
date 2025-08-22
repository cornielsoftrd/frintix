from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    """
    Permission that checks if the authenticated user has one of the allowed roles.
    Usage:
        permission_classes = [RolePermission(["role1", "role2"])]
    """
    allowed_roles = []
    #allowed_company=[]
    def has_permission(self, request, view):
        if not request or not hasattr(request, "user"):
            return False
        user = request.user
        if not getattr(user, "is_authenticated", False):
            return False
        return getattr(user, "role", None) in getattr(view, "allowed_roles", self.allowed_roles)
    


class IsRestaurantAdminOfTenant(permissions.BasePermission):
    message = "Only restaurant admins of this tenant can perform this action."

    def has_permission(self, request, view):
        user = request.user
        tenant = getattr(request, 'tenant', None)

        # Check user is authenticated, is restaurant_admin and belongs to tenant's company
        if not user.is_authenticated:
            return False

        if user.role != 'restaurant_admin':
            return False

        if not tenant or not hasattr(tenant, 'company'):
            return False

        # user must belong to the tenant company
        if user.company != tenant.company:
            return False

        return True