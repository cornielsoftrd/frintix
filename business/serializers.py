from rest_framework import serializers
from shared_core.models import User
from business.models import BusinessClient, Employee

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

    class Meta:
        model = BusinessClient
        fields = [
                'name',
                'email', 
                'password', 
                'address', 
                'phone',
                    
                    ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            email=email,
            password=password,
            is_businessaddmin=True,
            role='business_client'
        )
        return BusinessClient.objects.create(user=user, **validated_data)
    
# Employee Serializer
'''class EmployeeSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()  # permite crear usuario junto al empleado

    class Meta:
        model = Employee
        fields = ['id', 'user', 'business_client', 'allow_payroll', 'default_payment_method']
        extra_kwargs = {
            "business_client": {"read_only": True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        business_client = self.context["business_client"]
        user_data['role'] = 'employee'  # fuerza role empleado
        user = RegisterSerializer.create(RegisterSerializer(), validated_data=user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee'''

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'email', 'password', 'allow_payroll', 'default_payment_method']

        extra_kwargs = {
            "business_client": {"read_only": True}
        }

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user = User.objects.create_user(
            email=email,
            password=password,
            role="employee" 
        )
        employee = Employee.objects.create(
            user=user,
            #business_client=business_client,
            **validated_data
        )
        return employee
    
    