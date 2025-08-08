from rest_framework import viewsets, permissions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company = self.request.user.company

        # Employees see only their own orders
        if self.request.user.role == 'employee':
            return Order.objects.filter(
                employee__user=self.request.user,
                company=company
            )
        # Admins see all orders for their company
        return Order.objects.filter(company=company)

    def perform_create(self, serializer):
        employee = serializer.validated_data['employee']
        payment_method = serializer.validated_data['payment_method']

        # Payroll eligibility check
        if payment_method == 'payroll' and not employee.allow_payroll:
            raise serializers.ValidationError(
                "Employee not eligible for payroll payment"
            )

        # Ensure employee belongs to same company
        if employee.company != self.request.user.company:
            raise serializers.ValidationError(
                "Employee does not belong to your company"
            )

        serializer.save(company=self.request.user.company)

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        order = self.get_object()

        if order.is_paid:
            return Response(
                {'detail': 'Already paid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # In production, hook into a payment gateway; here it’s simplified
        order.is_paid = True
        order.save()

        return Response({
            'detail': 'Payment confirmed',
            'order_id': order.id
        })
