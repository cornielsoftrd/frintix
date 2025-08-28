from django.db import models
from django.conf import settings
from business.models import BusinessClient, Employee
from shared_core.models import User
from business.models import Employee
from tenant_apps.catalog.models import Product, Combo, Menu
from shared_core.models import Company
from retail_customer.models import RetailCustomer
import uuid #tis is to generate a uuid for the order id so we can make the order GET public for this model so anyone with the address can see the order 





from django.db import models
from business.models import BusinessClient, Employee
from tenant_apps.catalog.models import Product, Combo, Menu
from shared_core.models import Company
from retail_customer.models import RetailCustomer


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('payroll', 'Payroll'),
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")
    business_client = models.ForeignKey(BusinessClient, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")
    retail_customer = models.ForeignKey(RetailCustomer, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")
    
    
    delivery_address = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)  # optional, can remove
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    is_paid = models.BooleanField(default=False)
    is_paid_by_business = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ordered_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-ordered_at']

    def __str__(self):
        who = self.employee.user.email if self.employee else \
              self.retail_customer.user.email if self.retail_customer else "Unknown"
        return f"Order #{self.id} by {who}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    combo = models.ForeignKey(Combo, on_delete=models.SET_NULL, null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_price(self):
        if self.product:
            return self.product.price * self.quantity
        if self.combo:
            return self.combo.price * self.quantity
        if self.menu:
            return self.menu.price * self.quantity
    print(item_price)
        

    def __str__(self):
        return f"Item {self.id} of Order {self.order.id}"

   
