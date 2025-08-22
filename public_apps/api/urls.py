from django.urls import path
from ..views import TenantCreateAPIView

urlpatterns = [
    path('signup/', TenantCreateAPIView.as_view(), name='tenant-signup'),
]
