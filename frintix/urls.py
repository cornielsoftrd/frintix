"""
URL configuration for frintix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),

    # Public tenant registration, etc.
    path('api/public/', include('public_apps.api.urls')),

    # Auth API
    path('', include('tenant_apps.api.urls')),

    # Catalog API (products, combos, menus)
    #path('api/catalog/', include('tenant_apps.catalog.urls')),

    # Orders API
    #path('api/orders/', include('tenant_apps.orders.urls')),

    # Business Clients API
    #path('api/business/', include('tenant_apps.business.urls')),

    # Billing API
    path('api/billing/', include('tenant_apps.billing.urls')),

 
]


