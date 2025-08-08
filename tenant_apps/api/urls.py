from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from tenant_apps.api.views import RegisterView, CustomTokenObtainPairView
from tenant_apps.business.views import (
    BusinessClientViewSet,
    BusinessClientListCreateView,
    EmployeeListCreateView,
    EmployeeCreateView,
    BusinessClientDetailView
)

router = DefaultRouter()
router.register(r'business-clients', BusinessClientViewSet, basename='business-client')

urlpatterns = [
    # Auth
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Business Clients
    path('api/business_clients/', BusinessClientListCreateView.as_view(), name='business-client-list-create'),
    path('api/business_clients/<int:pk>/', BusinessClientDetailView.as_view(), name='business-client-detail'),

    # Employees
    path('api/employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('api/employees/create/', EmployeeCreateView.as_view(), name='create-employee'),

    # Catalog, Orders, Billing etc. (como ya tienes)
    path('api/catalog/', include('tenant_apps.catalog.urls')),
    path('api/orders/', include('tenant_apps.orders.urls')),
    path('api/billing/', include('tenant_apps.billing.urls')),
]
