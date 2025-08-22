from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RetailCustomerRegisterView

router = DefaultRouter()


urlpatterns = [
    path('register/', RetailCustomerRegisterView.as_view(), name='retail-register'),
]

urlpatterns += router.urls
