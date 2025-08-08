from rest_framework import viewsets, permissions, generics
from .models import BusinessClient, Employee
from .serializers import BusinessClientSerializer, EmployeeSerializer, EmployeeCreateSerializer
from shared_core.models import User

class BusinessClientViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessClientSerializer
    queryset = BusinessClient.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # restaurant admin sees all business clients in this tenant
        return BusinessClient.objects.all()

class EmployeeCreateView(generics.CreateAPIView):
    serializer_class = EmployeeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # only allow restaurant admin or business_admin? We'll check role
        if self.request.user.role != 'restaurant_admin' and self.request.user.role != 'business_admin':
            raise PermissionError("Only admins can create employees")
        serializer.save()
