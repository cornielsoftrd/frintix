from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self): return self.name

class Combo(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='combos')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self): return self.name

class Menu(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    products = models.ManyToManyField(Product, blank=True)
    combos = models.ManyToManyField(Combo, blank=True)
