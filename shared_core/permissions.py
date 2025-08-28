from rest_framework import permissions
 
    
from rest_framework import permissions

class IsBusinessAdmin(permissions.BasePermission):
    message = "Only business admins of this business can perform this action."

    def has_permission(self, request, view):
        user = request.user

        # Must be authenticated
        if not user.is_authenticated:
            return False

        # Must have the correct role
        if getattr(user, "role", None) != "business_client":
            return False

        # Must have the business admin flag
        if not getattr(user, "is_businessadmin", False):
            return False

        # Must be linked to a business client
        if not hasattr(user, "business_client") or user.business_client is None:
            return False

        return True

    
    