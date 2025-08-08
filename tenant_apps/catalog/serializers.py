from rest_framework import serializers
from .models import Product, Combo, Menu


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'company']


class ComboSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Combo
        fields = '__all__'
        read_only_fields = ['id', 'company']


class MenuSerializer(serializers.ModelSerializer):
    combos = ComboSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ['id', 'company']
