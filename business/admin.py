from django.contrib import admin

# Register your models here.
from business.models import BusinessClient,Employee,EmployeeOrderSummary

admin.site.register(BusinessClient)
admin.site.register(Employee)
admin.site.register(EmployeeOrderSummary)

