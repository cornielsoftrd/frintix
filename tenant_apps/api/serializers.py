from django.db import connection
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist

from shared_core.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # For confirmation

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data, company=None):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        #Remueve username si está en validated_data
        validated_data.pop('username', None)

        user = User.objects.create_user(email=email,company=company, password=password, **validated_data)
        return user
        


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        current_tenant = connection.tenant

        if user.role == 'restaurant_admin' and hasattr(user, 'business_client'):
            if user.business_client.name != current_tenant.name:
                raise AuthenticationFailed("User does not belong to this tenant.")
            
        # Add user info to the response
        data['user'] = {
            "id": user.id,
            "email": user.email,
            "name": user.get_full_name() or user.email,  # or username if you prefer
        }

        return data
        