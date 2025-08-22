from rest_framework import permissions

from rest_framework.permissions import BasePermission


def RolePermission(allowed_roles=None):
    allowed_roles = set(allowed_roles or [])

    class _RolePermission(BasePermission):
        def has_permission(self, request, view):
            user = request.user
            if not user or not user.is_authenticated:
                return False
            return getattr(user, "role", None) in allowed_roles

        def has_object_permission(self, request, view, obj):
            # Tenant check via product/combo/menu company linked to user's company (tenant)
            user_company = getattr(request.user, 'company', None)

            def get_obj_company(order_obj):
                for item in [order_obj.product, order_obj.combo, order_obj.menu]:
                    if item and hasattr(item, 'company'):
                        return item.company
                return None

            obj_company = get_obj_company(obj)
            return user_company is not None and obj_company == user_company

    return _RolePermission



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