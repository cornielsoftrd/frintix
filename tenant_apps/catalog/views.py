from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from tenant_apps.catalog.permissions import RolePermission,IsRestaurantAdminOfTenant
from .models import Product, Combo, Menu
from .serializers import ProductSerializer, ComboSerializer, MenuSerializer


# ---------- PRODUCT VIEWSET ----------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [IsRestaurantAdminOfTenant]
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Return only products belonging to user's tenant company
        tenant = getattr(self.request, 'tenant', None)
        if tenant and hasattr(tenant, 'company'):
            return Product.objects.filter(company=tenant.company)
        return Product.objects.none()

    def perform_create(self, serializer):
        # Force the product's company to be the tenant company (ignore any input company)
        tenant = getattr(self.request, 'tenant', None)
        if tenant and hasattr(tenant, 'company'):
            serializer.save(company=tenant.company)
        else:
            raise PermissionDenied("Tenant company not found.")

 

class ComboViewSet(viewsets.ModelViewSet):
    serializer_class = ComboSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Combo.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
