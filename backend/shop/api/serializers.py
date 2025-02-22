# shop/api/serializers.py
from rest_framework import serializers
from shop.models import Product, Panorama, Hotspot

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # o ['id', 'name', 'price', 'description', 'image']

class HotspotSerializer(serializers.ModelSerializer):
    # Para mostrar info del producto vinculado si quieres (opcional)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Hotspot
        fields = '__all__'

class PanoramaSerializer(serializers.ModelSerializer):
    # Incluye hotspots anidados
    hotspots = HotspotSerializer(many=True, read_only=True)

    class Meta:
        model = Panorama
        fields = '__all__'
