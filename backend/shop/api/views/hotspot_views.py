# backend/shop/api/views/hotspot_views.py
from rest_framework import viewsets
from shop.models import Hotspot
from shop.api.serializers.hotspot_serializers import HotspotSerializer
from shop.api.permissions import IsAdminOrManagerOrReadOnly

class HotspotViewSet(viewsets.ModelViewSet):
    queryset = Hotspot.objects.all()
    serializer_class = HotspotSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
