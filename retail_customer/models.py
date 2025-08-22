from django.db import models
from django.conf import settings

class RetailCustomer(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        #('paypal', 'PayPal'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash'
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"
