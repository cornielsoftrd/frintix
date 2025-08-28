from rest_framework import serializers
from .models import RetailCustomer
from shared_core.models import User

class RetailCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RetailCustomer
        fields = [
            "user",
            "phone",
            "country",
            "city",
            "street",
            "zip_code",
            "payment_method",
            "created_att"
        ]


class RetailCustomerRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    # New structured fields for address
    country = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    street = serializers.CharField(required=False, allow_blank=True)
    zip_code = serializers.CharField(required=False, allow_blank=True)

    payment_method = serializers.ChoiceField(
        choices=[('cash','Cash'),('credit_card','Credit Card')],
        default='cash'
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        phone = validated_data.pop('phone', None)
        country = validated_data.pop('country', '')
        city = validated_data.pop('city', '')
        street = validated_data.pop('street', '')
        zip_code = validated_data.pop('zip_code', '')
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
            country=country,
            city=city,
            street=street,
            zip_code=zip_code,
            payment_method=payment_method
        )
        return retail_customer