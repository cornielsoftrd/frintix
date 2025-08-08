from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ComboViewSet, MenuViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'combos', ComboViewSet, basename='combo')
router.register(r'menus', MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
]
