# tenant_apps/b2b/models.py
from django.conf import settings
from django.db import models
from shared_core.models import Company, User
 

class BusinessClient(models.Model):
    #company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="business_client", blank=True, null=True)
    name = models.CharField(max_length=260)
    email = models.EmailField(blank=True, null=True)
    #address = models.CharField(max_length=100,blank=True, null=True)
    phone = models.CharField(max_length=50,blank=True, null=True)
    
    # --- Replaced the single 'location' field with more structured fields ---
    country = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Country"
    )
    city = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="City"
    )
    street = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Street Address"
    )
    zip_code = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Zip Code"
    )
    
    
    default_payment_method = models.CharField(
    max_length=20,
        choices=[ ('cash', 'Cash'), ('credit_card', 'Credit Card')],
        default='credit_card'
    )

    created_att=models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_client = models.ForeignKey(BusinessClient, on_delete=models.CASCADE, related_name='employees')
    allow_payroll = models.BooleanField(default=True)

      # --- Replaced the single 'location' field with more structured fields ---
    country = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Country"
    )
    city = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="City"
    )
    street = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Street Address"
    )
    zip_code = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Zip Code"
    )
    

    default_payment_method = models.CharField(
        max_length=20,
        choices=[('payroll', 'Payroll'), ('cash', 'Cash'), ('credit_card', 'Credit Card')],
        default='payroll'
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.email
    

class EmployeeOrderSummary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='order_summaries')
    business_client = models.ForeignKey(BusinessClient, on_delete=models.CASCADE, related_name='employee_summaries')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    last_order_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'business_client')

    def __str__(self):
        return f"{self.employee.user.get_full_name()} ({self.business_client.name})"
    

#Notes:
#total_amount → sum of all orders paid via payroll or relevant method
#total_orders → count of orders
#last_order_at → timestamp of last order