from rest_framework import serializers
from public_apps.models import Client, Domain, Company
from shared_core.models import User
from django.db import transaction

class TenantCreateSerializer(serializers.Serializer):
    schema_name = serializers.CharField()
    company_name = serializers.CharField()
    domain = serializers.CharField()
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if Client.objects.filter(schema_name=data['schema_name']).exists():
            raise serializers.ValidationError("Schema name already exists")
        if Domain.objects.filter(domain=data['domain']).exists():
            raise serializers.ValidationError("Domain already exists")
        return data

    def create(self, validated_data):
        with transaction.atomic():
            company = Company.objects.create(name=validated_data['company_name'])

            tenant = Client(schema_name=validated_data['schema_name'],
                            name=validated_data['company_name'],
                            company=company)
            tenant.save()

            domain = Domain(domain=validated_data['domain'], tenant=tenant, is_primary=True)
            domain.save()

            admin_user = User.objects.create_superuser(
                email=validated_data['admin_email'],
                password=validated_data['admin_password'],
                role='restaurant_admin',
                company=company
            )
            return tenant



class TenantListSerializer(serializers.ModelSerializer):
    primary_domain = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'schema_name', 'primary_domain']

    def get_primary_domain(self, obj):
        domain = Domain.objects.filter(tenant=obj, is_primary=True).first()
        return domain.domain if domain else None