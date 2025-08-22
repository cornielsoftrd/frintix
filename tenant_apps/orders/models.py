from django.db import models
from django.conf import settings
from business.models import BusinessClient, Employee
from shared_core.models import User
from business.models import Employee
from tenant_apps.catalog.models import Product, Combo, Menu
from shared_core.models import Company
from retail_customer.models import RetailCustomer





class Order(models.Model):
    PAYMENT_CHOICES = [
        ('payroll', 'Payroll'),
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Business client (only set if order is placed by an employee)
    business_client = models.ForeignKey(
        BusinessClient, 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name="orders"
    )

    # who placed the order
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name="orders"
    )
    retail_customer = models.ForeignKey(
        RetailCustomer, 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name="orders"
    )

    delivery_address = models.TextField(blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    combo = models.ForeignKey(Combo, on_delete=models.SET_NULL, null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    is_paid = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ordered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ordered_at']

    def __str__(self):
        who = None
        if self.employee:
            who = self.employee.user.email
        elif self.retail_customer:
            who = self.retail_customer.user.email
        else:
            who = "Unknown"

        item = self.product or self.combo or self.menu or "No item"
        return f"Order #{self.id} by {who} - {item}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    combo = models.ForeignKey(Combo, on_delete=models.SET_NULL, null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item {self.id} of Order {self.order.id}"