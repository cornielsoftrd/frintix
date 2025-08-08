from rest_framework import serializers
from .models import BusinessClient, Employee
from shared_core.models import User

class BusinessClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessClient
        fields = '__all__'

class EmployeeCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    business_client = serializers.PrimaryKeyRelatedField(queryset=BusinessClient.objects.all())

    def create(self, validated_data):
        # create shared user then Employee
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
            role='employee'
        )
        employee = Employee.objects.create(user=user, business_client=validated_data['business_client'])
        return employee

class EmployeeSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Employee
        fields = ['id','user_email','business_client','allow_payroll','default_payment_method']
