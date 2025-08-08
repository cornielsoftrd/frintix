from rest_framework import serializers
from shared_core.models import User, Company
from tenant_apps.business.models import BusinessClient, Employee

# User Serializer (register)
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'role', 'company']
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

# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()  # permite crear usuario junto al empleado

    class Meta:
        model = Employee
        fields = ['id', 'user', 'business_client', 'allow_payroll', 'default_payment_method']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'employee'  # fuerza role empleado
        user = RegisterSerializer.create(RegisterSerializer(), validated_data=user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
