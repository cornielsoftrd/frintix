from django.db import models
from shared_core.models import Company  # your company model

class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.id} - {self.company.name} - ${self.amount}"
