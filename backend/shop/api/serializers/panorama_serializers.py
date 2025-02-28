# backend/shop/api/serializers/panorama_serializers.py
from rest_framework import serializers
from shop.models import Panorama
from shop.api.serializers.hotspot_serializers import HotspotSerializer

class PanoramaSerializer(serializers.ModelSerializer):
    hotspots = HotspotSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Panorama
        fields = '__all__'
