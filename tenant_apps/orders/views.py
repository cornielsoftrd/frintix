from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django_tenants.utils import schema_context
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
        if user.role in ['restaurant_admin', 'business_admin']:
            return True
        return False

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderOwnerOrAdmin]

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
            if user.role == 'restaurant_admin':
                return Order.objects.all()
            return Order.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        tenant = getattr(self.request, 'tenant', None)
        if not tenant:
            raise PermissionDenied("You must specify a tenant to place an order")

        with schema_context(tenant.schema_name):
            # Ensure user is only ordering from one tenant at a time
            existing_orders = Order.objects.filter(
                employee__user=user if hasattr(user, 'employee') else None,
                status='pending'
            )
            if existing_orders.exists():
                first_order_tenant = existing_orders.first().business_client.company
                if first_order_tenant != tenant.company:
                    raise PermissionDenied("You can only place orders for one tenant at a time.")

            if hasattr(user, 'employee'):
                employee = user.employee
                business_client = employee.business_client
                serializer.save(employee=employee, business_client=business_client)
            elif hasattr(user, 'retailcustomer'):
                retail_customer = user.retailcustomer
                serializer.save(retail_customer=retail_customer)
            else:
                serializer.save()

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        tenant = getattr(request, 'tenant', None)
        if not tenant:
            return Response({'detail': 'Tenant not set'}, status=status.HTTP_400_BAD_REQUEST)

        with schema_context(tenant.schema_name):
            order = self.get_object()
            if order.is_paid:
                return Response({'detail': 'Already paid'}, status=status.HTTP_400_BAD_REQUEST)
            order.is_paid = True
            order.status = 'processing'
            order.save()
            return Response({'detail': 'Payment confirmed', 'order_id': order.id})
