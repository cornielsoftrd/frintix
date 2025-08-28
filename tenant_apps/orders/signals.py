# tenant_apps/orders/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_tenants.utils import schema_context
from .models import Order,OrderItem
from business.models import EmployeeOrderSummary

def update_employee_summary(order):
    """
    Recalculate EmployeeOrderSummary for a given order's employee and business client.
    """
    if not order.employee or not order.business_client:
        return

    # Calculate totals for all orders of this employee in this tenant
    orders = Order.objects.filter(
        employee=order.employee,
        business_client=order.business_client
    )

    total_amount = sum(o.total_price for o in orders)  # <-- use total_price
    total_orders = orders.count()
    last_order_at = orders.order_by('-ordered_at').first().ordered_at if orders.exists() else None

    # Update public summary table
    from django_tenants.utils import schema_context
    with schema_context('public'):
        summary, _ = EmployeeOrderSummary.objects.get_or_create(
            employee=order.employee,
            business_client=order.business_client
        )
        summary.total_amount = total_amount
        summary.total_orders = total_orders
        summary.last_order_at = last_order_at
        summary.save()


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, **kwargs):
    update_employee_summary(instance)


@receiver(post_delete, sender=Order)
def order_post_delete(sender, instance, **kwargs):
    update_employee_summary(instance)


# --- Update summary when an OrderItem is created, updated, or deleted ---
@receiver(post_save, sender=OrderItem)
def orderitem_post_save(sender, instance, **kwargs):
    # Recalculate parent order's total_price first
    order = instance.order
    order.total_price = sum(item.item_price for item in order.items.all())
    order.save(update_fields=['total_price'])

    # Update employee summary
    update_employee_summary(order)


@receiver(post_delete, sender=OrderItem)
def orderitem_post_delete(sender, instance, **kwargs):
    order = instance.order
    order.total_price = sum(item.item_price for item in order.items.all())
    order.save(update_fields=['total_price'])

    update_employee_summary(order)