# cart/serializers.py

from rest_framework import serializers
from shop.models import Cart, CartItem
from shop.models import Product
from shop.api.serializers.product_serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    # Mostrar info completa del producto al leer
    product = ProductSerializer(read_only=True)
    # Permitir setear el producto por su ID al crear/actualizar
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'quantity', 'subtotal')

class CartSerializer(serializers.ModelSerializer):
    # Anidar los CartItem
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'is_active', 'items', 'total')
        read_only_fields = ('user', 'items', 'total')
