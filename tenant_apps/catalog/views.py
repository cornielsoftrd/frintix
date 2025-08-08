from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product, Combo, Menu
from .serializers import ProductSerializer, ComboSerializer, MenuSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


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
