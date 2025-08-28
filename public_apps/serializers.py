# tenants/serializers.py

from rest_framework import serializers
from public_apps.models import Client, Domain, Company
from shared_core.models import User
from django.db import transaction
import re

def clean_phone_number(input_string):
    # format the numbers to Keep only digits 0-9 
    cleaned_string = re.sub(r'[^0-9]', '', input_string)
    return cleaned_string

class TenantCreateSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    admin_first_name = serializers.CharField() 
    admin_last_name = serializers.CharField()   
    phone_number = serializers.CharField()
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True)

    #------ Address Fields-----
    country = serializers.CharField()
    city = serializers.CharField()
    street = serializers.CharField()
    zip_code = serializers.CharField()

    def validate(self, data):
        errors = {}

        # Generate schema_name and domain_name
        schema_name = data['company_name'].lower().replace(' ', '')
        domain_name = f"{schema_name}.localhost"

        if Client.objects.filter(schema_name=schema_name).exists():
            errors['company_name'] = "A company with this name already exists."
        if Domain.objects.filter(domain=domain_name).exists():
            errors['company_name'] = "A domain for this company already exists."
        if User.objects.filter(email=data['admin_email']).exists():
            errors['admin_email'] = "A user with this email already exists."

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        schema_name = validated_data['company_name'].lower().replace(' ', '')
        domain_name = f"{schema_name}.localhost"
        phone_number = validated_data['phone_number']

        with transaction.atomic():
            # Create company
            company = Company.objects.create(name=validated_data['company_name'])

            # Create tenant
            tenant = Client(
                schema_name=schema_name,
                name=validated_data['company_name'],
                phone=clean_phone_number(phone_number),
                company=company,
                country=validated_data['country'],
                city=validated_data['city'],
                street=validated_data['street'],
                zip_code=validated_data['zip_code']
            )
            tenant.save()

            # Create domain
            domain = Domain(domain=domain_name, tenant=tenant, is_primary=True)
            domain.save()

            # Create admin user
            admin_user = User.objects.create_superuser(
                email=validated_data['admin_email'],
                password=validated_data['admin_password'],
                role='restaurant_admin',
                company=company,
                first_name=validated_data['admin_first_name'],
                last_name=validated_data['admin_last_name'],
                is_staff=False,
                is_superuser=False
            )

            return tenant
class TenantListSerializer(serializers.ModelSerializer):
    primary_domain = serializers.SerializerMethodField()

    class Meta:
        model = Client
        # --- Add the new fields here and remove the old 'location' field ---
        fields = ['id', 'name', 'schema_name', 'primary_domain', 'country', 'city', 'street', 'zip_code']

    def get_primary_domain(self, obj):
        domain = Domain.objects.filter(tenant=obj, is_primary=True).first()
        return domain.domain if domain else None