# tenants/models.py

from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from shared_core.models import Company

class Client(TenantMixin):
    """Tenant que representa a un restaurante."""
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

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

    auto_create_schema = True

    def save(self, *args, **kwargs):
        if not self.company_id:
            company = Company.objects.create(name=self.name)
            self.company = company
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass