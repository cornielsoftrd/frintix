from django.contrib import admin

# Register your models here.
from business.models import BusinessClient,Employee

admin.site.register(BusinessClient)
admin.site.register(Employee)

