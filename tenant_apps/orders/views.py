from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django_tenants.utils import schema_context
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser
from .models import Order
from .serializers import OrderSerializer


class IsOrderOwnerOrAdmin(permissions.BasePermission):
    """Owner (employee/retail) or admin permission."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'employee') and obj.employee and obj.employee.user == user:
            return True
        if hasattr(user, 'retailcustomer') and obj.retail_customer and obj.retail_customer.user == user:
            return True
        if getattr(user, "role", None) in ['restaurant_admin', 'business_admin']:
            return True
        return False


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        tenant = getattr(self.request, 'tenant', None)
        if not tenant:
            return Order.objects.none()

        with schema_context(tenant.schema_name):
            if hasattr(user, 'employee'):
                return Order.objects.filter(employee__user=user)
            if hasattr(user, 'retailcustomer'):
                return Order.objects.filter(retail_customer__user=user)
            if getattr(user, "role", None) == 'restaurant_admin':
                return Order.objects.all()
            return Order.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        tenant = getattr(self.request, 'tenant', None)
        if not tenant:
            raise PermissionDenied("You must specify a tenant to place an order")

        with schema_context(tenant.schema_name):
            if hasattr(user, 'employee'):
                employee = user.employee
                business_client = employee.business_client
                serializer.save(employee=employee, business_client=business_client)
            elif hasattr(user, 'retailcustomer'):
                retail_customer = user.retailcustomer
                serializer.save(retail_customer=retail_customer)
            else:
                serializer.save()


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    #permission_classes = [permissions.IsAuthenticated, IsOrderOwnerOrAdmin]
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"  # use UUID instead of pk

    def get_queryset(self):
        user = self.request.user
        tenant = getattr(self.request, 'tenant', None)

        # Return empty queryset if no tenant or user is anonymous
        if not tenant or isinstance(user, AnonymousUser):
            return Order.objects.none()

        with schema_context(tenant.schema_name):
            # Restaurant admin sees all orders
            if getattr(user, "role", None) == 'restaurant_admin':
                return Order.objects.all()

            # Employees or retail customers see only their own orders
            return Order.objects.filter(employee__user=user) | Order.objects.filter(retail_customer__user=user)


class ConfirmPaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrderOwnerOrAdmin]

    def post(self, request, uuid):
        tenant = getattr(request, 'tenant', None)
        if not tenant:
            return Response({'detail': 'Tenant not set'}, status=status.HTTP_400_BAD_REQUEST)

        with schema_context(tenant.schema_name):
            try:
                order = Order.objects.get(uuid=uuid)
            except Order.DoesNotExist:
                return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

            self.check_object_permissions(request, order)

            if order.is_paid:
                return Response({'detail': 'Already paid'}, status=status.HTTP_400_BAD_REQUEST)

            order.is_paid = True
            order.status = 'processing'
            order.save()
            return Response({'detail': 'Payment confirmed', 'order_uuid': order.uuid})

 
