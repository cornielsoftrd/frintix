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
    #address = models.TextField(blank=True, null=True)

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

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash'
    )

    created_att=models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"
