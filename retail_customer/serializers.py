from rest_framework import serializers
from .models import RetailCustomer
from shared_core.models import User

class RetailCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RetailCustomer
        fields = '__all__'


class RetailCustomerRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(
        choices=[('cash','Cash'),('credit_card','Credit Card'),('paypal','PayPal')],
        default='cash'
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        phone = validated_data.pop('phone', None)
        address = validated_data.pop('address', None)
        payment_method = validated_data.pop('payment_method', 'cash')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role='retail_customer'
        )

        retail_customer = RetailCustomer.objects.create(
            user=user,
            phone=phone,
            address=address,
            payment_method=payment_method
        )
        return retail_customer