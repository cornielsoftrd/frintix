from rest_framework import permissions
 
    
class IsBusinessAdmin(permissions.BasePermission):
    message = "Only Busness admins of this Business can perform this action."

    def has_permission(self, request, view):
        user = request.user
        

        # Check user is authenticated, is restaurant_admin and belongs to tenant's company
        if not user.is_authenticated:
            return False

        if user.role != 'business_client':
            return False
 
        # user must be a business admin
        if request.user.is_businessadmin != True:
            return False
        
        if not hasattr(user, "business_client"):
             return False
        
       

        return True
    
    