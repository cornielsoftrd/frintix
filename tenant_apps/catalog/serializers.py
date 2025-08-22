from rest_framework import serializers
from .models import Product, Combo, Menu


from rest_framework import serializers
from tenant_apps.catalog.models import Product
from tenant_apps.orders.models import Order

from retail_customer.models import RetailCustomer

# ---------- PRODUCT SERIALIZER ----------
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['company']

   

    def create(self, validated_data):
        
        request = self.context.get('request')
        if request and hasattr(request, 'tenant'):
            validated_data['company'] = request.tenant.company
        return super().create(validated_data)


# ---------- ORDER SERIALIZER ----------
class OrderSerializer(serializers.ModelSerializer):
    retail_customer_email = serializers.EmailField(source='retail_customer.user.email', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['company', 'employee', 'ordered_at']

    def validate(self, data):
        product = data.get('product')
        combo = data.get('combo')
        menu = data.get('menu')

        selected = [x for x in [product, combo, menu] if x]
        if len(selected) > 1:
            raise serializers.ValidationError(
                "Solo se puede seleccionar uno entre producto, combo o menú."
            )

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'tenant'):
            validated_data['company'] = request.tenant
        return super().create(validated_data)




class ComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = ['id', 'name', 'products', 'price', 'description']

 
    
    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        validated_data.pop('company', None)  # remove if present

        tenant_company = getattr(self.context['request'].tenant, 'company', None)
        if not tenant_company:
            raise ValidationError("Cannot determine current tenant company")

        combo = Combo.objects.create(
            company=tenant_company,  # must be a Company instance
            **validated_data
        )
        combo.products.set(products_data)
        return combo
       

class MenuSerializer(serializers.ModelSerializer):
    combos = ComboSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ['id', 'company']
