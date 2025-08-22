from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BusinessClientViewSet, 
    EmployeeListCreateView, 
    BusinessClientRegisterView,
    BusinessClientListCreateView,
    BusinessClientDetailView
    )

router = DefaultRouter()
#router.register('business-clients', BusinessClientViewSet, basename='business-client')

urlpatterns = [
    path('', include(router.urls)),
    path('api/business/register', BusinessClientRegisterView.as_view(), name='register-bussinessCient'),
    path('api/employees/create/', EmployeeListCreateView.as_view(), name='create-employee'),
     # Business Clients
    #path('api/business_clients/', BusinessClientListCreateView.as_view(), name='business-client-list-create'),
    path('api/business_clients/<int:pk>/', BusinessClientDetailView.as_view(), name='business-client-detail'),
]
