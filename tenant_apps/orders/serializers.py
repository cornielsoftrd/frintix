# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from tenant_apps.catalog.models import Product, Combo, Menu
from business.models import Employee, BusinessClient
from retail_customer.models import RetailCustomer

# --- Nested serializers for output ---
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

# --- OrderItem serializer ---
class OrderItemSerializer(serializers.ModelSerializer):
    item_price = serializers.SerializerMethodField()  # computed on backend

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'combo', 'menu', 'quantity', 'item_price']

    def get_item_price(self, obj):
        if obj.product:
            return obj.product.price
        elif obj.combo:
            return obj.combo.price
        elif obj.menu:
            return obj.menu.price
        return 0

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

# --- Main Order serializer ---
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    employee = EmployeeSimpleSerializer(read_only=True)
    retail_customer = RetailCustomerSimpleSerializer(read_only=True)
    business_client = BusinessClientSimpleSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()  # total calculated on backend
    tenant = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'uuid', 'items', 'is_paid', 'status', 'ordered_at',
            'employee', 'retail_customer', 'business_client',
            'delivery_address', 'payment_method', 'company', 'total_price', 'tenant'
        ]
        read_only_fields = ['is_paid', 'status', 'ordered_at', 'company', 'uuid',  'is_paid_by_business']

    def get_total_price(self, obj):
        return sum(item.item_price for item in obj.items.all())

    def get_tenant(self, obj):
        client = obj.company.client_set.first()
        if client:
            domain = client.get_primary_domain()
            return {
                "id": client.id,
                "name": client.name,
                "schema_name": client.schema_name,
                "apiUrl": f"http://{domain.domain}:8000/api" if domain else None
            }
        return None

    def validate(self, attrs):
        tenant = getattr(self.context['request'], 'tenant', None)
        user = getattr(self.context['request'], 'user', None)

        if not tenant:
            raise serializers.ValidationError("Tenant not found in request.")

        items = attrs.get('items', [])
        for item in items:
            product = item.get('product')
            combo = item.get('combo')
            menu = item.get('menu')
            item_company = None
            if product:
                item_company = product.company
            elif combo:
                item_company = combo.company
            elif menu:
                item_company = menu.company

            if not (user and user.role == "employee") and item_company != tenant.company:
                raise serializers.ValidationError("All items must belong to the current tenant.")
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        user = self.context['request'].user
        tenant = getattr(self.context['request'], 'tenant', None)

        # Assign company and user-specific relations
        if user.role != "employee" and tenant:
            validated_data['company'] = tenant.company
        elif user.role == "employee" and items_data:
            first_item = items_data[0]
            product = first_item.get('product')
            combo = first_item.get('combo')
            menu = first_item.get('menu')
            if product:
                validated_data['company'] = product.company
            elif combo:
                validated_data['company'] = combo.company
            elif menu:
                validated_data['company'] = menu.company
            validated_data['employee'] = user.employee
            validated_data['business_client'] = user.employee.business_client
        elif user.role == "retail_customer":
            validated_data['retail_customer'] = user.retail_customer

        # Create order
        order = Order.objects.create(**validated_data)

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
