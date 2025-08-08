from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils.text import slugify
from public_apps.models import Client, Domain
from shared_core.models import User
#from tenant_apps.core.models import ???  # if you had Company in tenant_apps; adapt accordingly

class RestaurantSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('company_name')
        email = request.data.get('email')
        password = request.data.get('password')
        subdomain = request.data.get('subdomain')  # required

        if not all([name,email,password,subdomain]):
            return Response({"error":"missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        schema_name = slugify(subdomain)
        try:
            with transaction.atomic():
                client = Client(schema_name=schema_name, name=name)
                client.save()  # will create schema because auto_create_schema=True
                Domain.objects.create(domain=f"{schema_name}.localhost", tenant=client, is_primary=True)

                # Create admin user inside tenant schema
                from django_tenants.utils import schema_context
                with schema_context(client.schema_name):
                    # create a shared_core.User but role 'restaurant_admin'
                    User.objects.create_user(email=email, password=password, role='restaurant_admin')
            return Response({'detail':'Restaurant and admin created'}, status=status.HTTP_201_CREATED)
        except Exception as exc:
            return Response({'error':str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TenantSignupView(APIView):
    def post(self, request):
        # Your tenant signup logic here
        return Response({"message": "Tenant created"}, status=status.HTTP_201_CREATED)