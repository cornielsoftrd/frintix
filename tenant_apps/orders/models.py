from django.db import models
from shared_core.models import User
from tenant_apps.business.models import Employee
from tenant_apps.catalog.models import Product, Combo, Menu
from tenant_apps.business.models import BusinessClient


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    company = models.ForeignKey(BusinessClient, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    combo = models.ForeignKey(Combo, on_delete=models.SET_NULL, null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.employee} - {self.status}"
