from rest_framework import serializers
from shared_core.models import User
from business.models import BusinessClient, Employee, EmployeeOrderSummary
from tenant_apps.orders.models import Order
from django.db.models import F, Sum
from public_apps.models import Client

# User Serializer (register)
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'role', ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

# BusinessClient Serializer
class BusinessClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessClient
        fields = '__all__'

class BusinessClientRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    country = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    street = serializers.CharField(write_only=True)
    zip_code = serializers.CharField(write_only=True)
    admin_first_name = serializers.CharField(write_only=True)
    admin_last_name = serializers.CharField(write_only=True)

    class Meta:
        model = BusinessClient
        fields = [
            'name',
            'email',
            'password',
            'phone',
            'country',
            'city',
            'street',
            'zip_code',
            'admin_first_name',
            'admin_last_name',
        ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('admin_first_name')
        last_name = validated_data.pop('admin_last_name')

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='business_client_admin'
        )
        return BusinessClient.objects.create(user=user, **validated_data)

# Employee Serializer
 

class EmployeeSerializer(serializers.ModelSerializer):
    # Fields for creating the linked User
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'allow_payroll',
            'default_payment_method',
            'country',
            'city',
            'street',
            'zip_code',
        ]
        extra_kwargs = {
            "business_client": {"read_only": True}
        }

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        # Create the User
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role="employee"
        )

        # Create Employee linked to User
        employee = Employee.objects.create(
            user=user,
            **validated_data
        )
        return employee
    
#summary of all orders made by employess
class EmployeeOrderSummarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    employee_email = serializers.CharField(source='employee.user.email', read_only=True)
    business_client_name = serializers.CharField(source='business_client.name', read_only=True)

    class Meta:
        model = EmployeeOrderSummary
        fields = ['employee', 'employee_name', 'employee_email', 'business_client', 'business_client_name', 'total_amount', 'total_orders', 'last_order_at','is_paid', 'is_paid_by_business']
    

 
from tenant_apps.orders.services import get_employee_orders_and_expenses


class EmployeeExpenseSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    total_spent = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'employee_name', 'email', 'total_spent', 'orders']

    def get_total_spent(self, obj):
        _, total_spent = get_employee_orders_and_expenses(obj)
        return total_spent

    def get_orders(self, obj):
        orders, _ = get_employee_orders_and_expenses(obj)
        order_list = []

        for order in orders:
            items_data = []
            for item in order.items.all():
                # Determine price of the item
                if item.product:
                    price = item.product.price
                    name = item.product.name
                elif item.combo:
                    price = item.combo.price
                    name = item.combo.name
                elif item.menu:
                    price = item.menu.price
                    name = item.menu.name
                else:
                    price = 0
                    name = None

                items_data.append({
                    "product": item.product.name if item.product else None,
                    "combo": item.combo.name if item.combo else None,
                    "menu": item.menu.name if item.menu else None,
                    "quantity": item.quantity,
                    "item_price": price,
                    "item_name": name
                     
                })

            order_total = sum(item["item_price"] * item["quantity"] for item in items_data)

            order_list.append({
                "id": order.id,
                "status": order.status,
                "payment_method": order.payment_method,
                "ordered_at": order.ordered_at,
                "delivery_address": order.delivery_address,
                "items": items_data,
                "order_total": order_total,

                "is_paid":order.is_paid, 
                "paid_by_business" :order.is_paid_by_business
                
            })

        return order_list
