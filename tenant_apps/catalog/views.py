from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from tenant_apps.catalog.permissions import IsRestaurantAdminOfTenant
from .models import Product, Combo, Menu
from .serializers import ProductSerializer, ComboSerializer, MenuSerializer


# ---------- PRODUCT VIEWSET ----------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return [AllowAny()]
        return [IsRestaurantAdminOfTenant()]  # or IsAuthenticated() if you prefer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant and hasattr(tenant, 'company'):
            return Product.objects.filter(company=tenant.company)
        return Product.objects.none()

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        if tenant and hasattr(tenant, 'company'):
            serializer.save(company=tenant.company)
        else:
            raise PermissionDenied("Permission Denied, Tenant company not found.")


# ---------- COMBO VIEWSET ----------
class ComboViewSet(viewsets.ModelViewSet):
    serializer_class = ComboSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Combo.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


# ---------- MENU VIEWSET ----------
class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
