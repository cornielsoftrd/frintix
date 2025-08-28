from django.urls import path
from .views import (
    OrderListCreateAPIView,
    OrderDetailAPIView,
    ConfirmPaymentAPIView,
   
)

urlpatterns = [
 
    path('api/orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('api/orders/<uuid:uuid>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('api/orders/<uuid:uuid>/confirm-payment/', ConfirmPaymentAPIView.as_view(), name='order-confirm-payment'),
]
