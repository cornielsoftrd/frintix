# public_apps/models.py
from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from shared_core.models import Company

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True, default='2025-09-09')
    on_trial = models.BooleanField(default=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # required by django-tenants
    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass
