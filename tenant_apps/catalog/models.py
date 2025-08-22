from django.db import models
from shared_core.models import Company

class Product(models.Model):
    """Producto del menú del restaurante."""
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Combo(models.Model):
    """Combo que agrupa varios productos."""
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='combos')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=1000,null=True,blank=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='combos', blank=True, null=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """Menú del día del restaurante."""
    name = models.CharField(max_length=255)
    date = models.DateField()
    products = models.ManyToManyField(Product, blank=True)
    combos = models.ManyToManyField(Combo, blank=True)

    def __str__(self):
        return f"{self.name} ({self.date})"
