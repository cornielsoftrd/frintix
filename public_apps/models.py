from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from shared_core.models import Company

class Client(TenantMixin):
    """Tenant que representa a un restaurante."""
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    auto_create_schema = True

    def save(self, *args, **kwargs):
        # Si no tiene company asignada, la crea en shared_core
        if not self.company_id:
            company = Company.objects.create(name=self.name)
            self.company = company
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass
