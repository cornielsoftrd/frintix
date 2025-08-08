from rest_framework import serializers
from .models import Order
from tenant_apps.business.models import Employee
from tenant_apps.catalog.models import Product, Combo, Menu


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['company', 'ordered_at', 'employee']

    def validate(self, data):
        product = data.get('product')
        combo = data.get('combo')
        menu = data.get('menu')

        # Only one type allowed
        selected = [x for x in [product, combo, menu] if x]
        if len(selected) > 1:
            raise serializers.ValidationError(
                "Only one of product, combo, or menu can be selected per order."
            )

        # Ensure selected item belongs to the same company
        company = self.context['request'].user.company
        for item in selected:
            if item.company != company:
                raise serializers.ValidationError(
                    f"{item.__class__.__name__} does not belong to your company."
                )

        return data
