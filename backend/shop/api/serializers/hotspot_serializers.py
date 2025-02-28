# backend/shop/api/serializers/hotspot_serializers.py
from rest_framework import serializers
from shop.models import Hotspot, Product, Panorama
from shop.api.serializers.product_serializers import ProductSerializer

class HotspotSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True,
        required=False
    )
    connected_panorama_id = serializers.PrimaryKeyRelatedField(
        queryset=Panorama.objects.all(),
        source='connected_panorama',
        write_only=True,
        required=False
    )

    class Meta:
        model = Hotspot
        fields = '__all__'
