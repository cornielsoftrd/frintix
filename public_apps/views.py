# tenants/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from django.db.models import Q
from public_apps.models import Client
from .serializers import TenantCreateSerializer, TenantListSerializer
import unicodedata

# client and tenant is the same entity

class ClientFilter(FilterSet):
    # This filter will now correctly handle accent and case-insensitive searches
    city = CharFilter(method='filter_by_normalized_city')

    class Meta:
        model = Client
        fields = ['city']

    def filter_by_normalized_city(self, queryset, name, value):
        if not value:
            return queryset
        
        # Normalize the search value to remove accents and convert to lowercase
        normalized_value = unicodedata.normalize('NFD', value).encode('ascii', 'ignore').decode('utf-8').lower()
        
        # Use a Q object to perform the search
        return queryset.filter(Q(city__icontains=normalized_value))


class TenantCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = TenantCreateSerializer(data=request.data)
        if serializer.is_valid():
            tenant = serializer.save()
            return Response({"detail": "Tenant created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TenantListAPIView(generics.ListAPIView):
    """
    Public endpoint to list all tenants (restaurants) with filtering.
    """
    queryset = Client.objects.all()
    serializer_class = TenantListSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [AllowAny]
    filterset_class = ClientFilter