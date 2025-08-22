from django.urls import path
from .views import TenantCreateAPIView,TenantListAPIView

urlpatterns = [
    
    path('create-tenant/', TenantCreateAPIView.as_view(), name='create-tenant'),
]
