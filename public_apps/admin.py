from django.contrib import admin
from .models import Client, Domain, Company
admin.site.register(Client)
admin.site.register(Domain)
admin.site.register(Company)
