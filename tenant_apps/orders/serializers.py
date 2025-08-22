from rest_framework import serializers
from .models import Order, OrderItem
from tenant_apps.catalog.models import Product, Combo, Menu
from business.models import Employee, BusinessClient
from retail_customer.models import RetailCustomer


# Nested serializers for output
class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class ComboSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = ['id', 'name', 'price']

class MenuSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'date']

class EmployeeSimpleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'email', 'first_name', 'last_name']

class BusinessClientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessClient
        fields = ['id', 'name']

class RetailCustomerSimpleSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = RetailCustomer
        fields = ['id', 'email', 'first_name', 'last_name']


# OrderItemSerializer with nested product/combo/menu
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'combo', 'menu', 'quantity']

    def validate(self, data):
        selected = [f for f in [data.get('product'), data.get('combo'), data.get('menu')] if f]
        if len(selected) == 0:
            raise serializers.ValidationError("You must select either a product, combo, or menu.")
        if len(selected) > 1:
            raise serializers.ValidationError("Only one of product, combo, or menu can be selected per item.")
        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.product:
            rep['product'] = ProductSimpleSerializer(instance.product).data
        if instance.combo:
            rep['combo'] = ComboSimpleSerializer(instance.combo).data
        if instance.menu:
            rep['menu'] = MenuSimpleSerializer(instance.menu).data
        return rep


# Main OrderSerializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    employee = EmployeeSimpleSerializer(read_only=True)
    retail_customer = RetailCustomerSimpleSerializer(read_only=True)
    business_client = BusinessClientSimpleSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'items', 'is_paid', 'status', 'ordered_at',
            'employee', 'retail_customer', 'business_client',
            'delivery_address',
        ]
        read_only_fields = ['is_paid', 'status', 'ordered_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
