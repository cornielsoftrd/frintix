from django.contrib import admin
from .models import Product,Combo, Menu
# Register your models here.
admin.site.register(Product)
admin.site.register(Combo)
admin.site.register(Menu)