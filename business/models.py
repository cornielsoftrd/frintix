# tenant_apps/b2b/models.py
from django.conf import settings
from django.db import models
from shared_core.models import Company, User

class BusinessClient(models.Model):
    #company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="business_client", blank=True, null=True)
    name = models.CharField(max_length=260)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    default_payment_method = models.CharField(
    max_length=20,
        choices=[ ('cash', 'Cash'), ('credit_card', 'Credit Card')],
        default='credit_card'
    )

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_client = models.ForeignKey(BusinessClient, on_delete=models.CASCADE, related_name='employees')
    allow_payroll = models.BooleanField(default=True)
    default_payment_method = models.CharField(
        max_length=20,
        choices=[('payroll', 'Payroll'), ('cash', 'Cash'), ('credit_card', 'Credit Card')],
        default='payroll'
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.email

