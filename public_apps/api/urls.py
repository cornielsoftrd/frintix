from django.urls import path
from ..views import TenantCreateAPIView,TenantListAPIView

urlpatterns = [
    path("tenants/", TenantListAPIView.as_view(), name="tenant-list"),
    path('signup/', TenantCreateAPIView.as_view(), name='tenant-signup'),
]
