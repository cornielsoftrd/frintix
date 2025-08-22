from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import TenantCreateSerializer

class TenantCreateAPIView(APIView):
    
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = TenantCreateSerializer(data=request.data)
        if serializer.is_valid():
            tenant = serializer.save()
            return Response({"detail": "Tenant created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
