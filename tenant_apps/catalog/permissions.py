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
    """
    Only allows access to restaurant_admin users of the current tenant.
    Requires request.tenant to be set by middleware.
    """
    message = "Only restaurant admins of this tenant can perform this action."

    def has_permission(self, request, view):
        user = request.user
        tenant = getattr(request, "tenant", None)

        # Debugging logs
        print("PERMISSION CHECK")
        print("user:", user, "role:", getattr(user, "role", None))
        print("tenant:", tenant)
        print("user.company:", getattr(user, "company", None))
        print("tenant.company:", getattr(tenant, "company", None))

        # Must be authenticated and role = restaurant_admin
        if not user.is_authenticated or user.role != "restaurant_admin":
            return False

        # Tenant must exist and have a company
        if not tenant or not hasattr(tenant, "company"):
            return False

        # Compare companies by ID (avoid object instance mismatch)
        if user.company.id != tenant.company.id:
            return False

        return True