from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tenant_apps.orders'
    def ready(self):
        
        import tenant_apps.orders.signals

 