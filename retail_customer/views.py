from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, permissions,status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import RetailCustomer
from .serializers import RetailCustomerSerializer,RetailCustomerRegisterSerializer

'''class RetailCustomerRegisterView(generics.CreateAPIView):
    serializer_class = RetailCustomerRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        retail_customer = serializer.save()
        output_serializer = RetailCustomerSerializer(retail_customer)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)'''


class RetailCustomerRegisterView(generics.CreateAPIView):
    serializer_class = RetailCustomerRegisterSerializer
    permission_classes = []  # AllowAny or custom if needed
    
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        retail_customer = serializer.save()
        user = retail_customer.user
        return Response({
            "id": retail_customer.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": retail_customer.phone,
            "country": retail_customer.country,
            "city": retail_customer.city,
            "street": retail_customer.street,
            "zip_code": retail_customer.zip_code,
            "payment_method": retail_customer.payment_method,
        }, status=status.HTTP_201_CREATED)
    

class RetailCustomerDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = RetailCustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.retailcustomer  # link User -> RetailCustomer