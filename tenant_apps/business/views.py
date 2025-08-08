from rest_framework import viewsets, generics, permissions
from shared_core.models import Company
from tenant_apps.business.models import BusinessClient, Employee
from .serializers import RegisterSerializer, BusinessClientSerializer, EmployeeSerializer


# Registro de usuario (incluye restaurant_admin y business_admin)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Listar/Crear Business Clients para un tenant
class BusinessClientListCreateView(generics.ListCreateAPIView):
    ueryset = BusinessClient.objects.all()
    serializer_class = BusinessClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Mostrar solo business clients del tenant company
        return BusinessClient.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

# Listar/Crear Employees para un BusinessClient
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        business_client_id = self.request.query_params.get('business_client')
        if business_client_id:
            return Employee.objects.filter(business_client_id=business_client_id)
        return Employee.objects.none()

    def perform_create(self, serializer):
        # validar que business_client es del tenant company del usuario
        business_client = serializer.validated_data['business_client']
        if business_client.company != self.request.user.company:
            raise PermissionDenied("Business client no pertenece a su empresa")
        serializer.save()
 
class BusinessClientViewSet(viewsets.ModelViewSet):
    queryset = BusinessClient.objects.all()
    serializer_class = BusinessClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo los business clients del tenant actual
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return BusinessClient.objects.filter(company=tenant)
        return BusinessClient.objects.none()

    def perform_create(self, serializer):
        tenant = getattr(self.request, 'tenant', None)
        print("Tenant in request:", tenant)
        serializer.save(company=tenant)


class BusinessClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessClient.objects.all()
    serializer_class = BusinessClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    


class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]