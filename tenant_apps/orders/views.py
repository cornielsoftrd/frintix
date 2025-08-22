from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class IsOrderOwnerOrAdmin(permissions.BasePermission):
    """
    Allow owners (employee/retail_customer) to see their orders; admins of business_client can see all.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        # employees can access own orders
        if hasattr(user, 'employee') and obj.employee and obj.employee.user == user:
            return True
        if hasattr(user, 'retailcustomer') and obj.retail_customer and obj.retail_customer.user == user:
            return True
        # business admins: if user is business_admin and belongs to same business_client
        if user.role in ['restaurant_admin', 'business_admin']:
            # allow for now; refine by company/business_client if needed
            return True
        return False
    

    #TODOLIST
    #Employee → automatically linked to their business_client Done
    #Business client → automatically set from the employee Done
    #Items → multiple items with nested product/combo details Cone
    #Retail customer → would be linked if a retail user created the order Done

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # employees see their own orders
        if hasattr(user, 'employee'):
            return Order.objects.filter(employee__user=user)
        # retail customers see their own orders
        if hasattr(user, 'retailcustomer'):
            return Order.objects.filter(retail_customer__user=user)
        # restaurant admins see all orders for their tenant
        if user.role == 'restaurant_admin':
            tenant = getattr(self.request, 'tenant', None)
            if tenant and getattr(tenant, 'company', None):
                return Order.objects.filter(business_client__company=tenant.company)
            return Order.objects.all()
        return Order.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
       

        if hasattr(user, 'employee'):
            employee = user.employee
            business_client = employee.business_client
            serializer.save(employee=employee, business_client=business_client)
        elif hasattr(user, 'retailcustomer'):
            retail_customer = user.retailcustomer
            serializer.save(retail_customer=retail_customer)
        else:
            # fallback, just save without linking
            serializer.save()

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        order = self.get_object()
        if order.is_paid:
            return Response({'detail': 'Already paid'}, status=status.HTTP_400_BAD_REQUEST)
        # here you would integrate with your payment gateway
        order.is_paid = True
        order.status = 'processing'
        order.save()
        return Response({'detail': 'Payment confirmed', 'order_id': order.id})