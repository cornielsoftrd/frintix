from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessClientViewSet, EmployeeCreateView

router = DefaultRouter()
router.register('business-clients', BusinessClientViewSet, basename='business-client')

urlpatterns = [
    path('', include(router.urls)),
    path('employees/create/', EmployeeCreateView.as_view(), name='create-employee'),
]
