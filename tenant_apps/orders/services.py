
from django.db.models import Sum
from django_tenants.utils import schema_context
from public_apps.models import Client
from .models import Order

#since the tenants are not accecible from the public, I created tis serice in the tenant so it can shar the tenants data with the public app, this way the business admin can see the employee expenses from the public app
#tat is because the orders lives in the tenant schechma wich is isolated
def get_employee_orders_and_expenses(employee):
    all_orders = []
    total_spent = 0

    for tenant in Client.objects.exclude(schema_name="public"):
        with schema_context(tenant.schema_name):
            # Force evaluation INSIDE the tenant context
            orders = list(
                    Order.objects.filter(employee=employee).prefetch_related("items__product", "items__combo", "items__menu")
                )

            spent = sum(order.total_price for order in orders)

            all_orders.extend(orders)
            total_spent += spent

    return all_orders, total_spent
