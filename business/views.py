from rest_framework import viewsets, generics, permissions
from shared_core.models import Company
from business.models import BusinessClient, Employee
from .serializers import RegisterSerializer, BusinessClientSerializer, EmployeeSerializer, EmployeeExpenseSerializer
from business.serializers import BusinessClientRegisterSerializer
from shared_core.permissions import IsBusinessAdmin
from rest_framework.exceptions import PermissionDenied
 
from tenant_apps.orders.services import get_employee_orders_and_expenses
 
 
from shared_core.permissions import IsBusinessAdmin

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
    serializer_class = EmployeeSerializer
    permission_classes = [IsBusinessAdmin]

    def get_queryset(self):
        """
        Return employees linked to the business client of the logged-in admin.
        """
        try:
            business_client = BusinessClient.objects.get(user=self.request.user)
        except BusinessClient.DoesNotExist:
            return Employee.objects.none()

        return Employee.objects.filter(business_client=business_client)

    def perform_create(self, serializer):
        """
        Automatically attach the new employee to the admin's business client.
        """
        try:
            business_client = BusinessClient.objects.get(user=self.request.user)
        except BusinessClient.DoesNotExist:
            raise PermissionDenied("You are not linked to any Business Client.")

        serializer.save(business_client=business_client)

#bussiness clint register
class BusinessClientRegisterView(generics.CreateAPIView):
    serializer_class = BusinessClientRegisterSerializer
    permission_classes = [permissions.AllowAny]


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
        #serializer.save(company=tenant)
        serializer.save(company=self.request.user.company)




class BusinessClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessClient.objects.all()
    serializer_class = BusinessClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    

class EmployeeExpensesView(generics.ListAPIView):
    serializer_class = EmployeeExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusinessAdmin]

    def get_queryset(self):
        business_client = getattr(self.request.user, "business_client", None)
        if not business_client:
            return Employee.objects.none()

        employees = Employee.objects.filter(business_client=business_client)

        for emp in employees:
            orders, total_spent = get_employee_orders_and_expenses(emp)
            emp._orders_cache = orders
            emp._total_spent_cache = total_spent

        return employees