# shop/api/views.py
from rest_framework import viewsets
from shop.models import Product, Panorama, Hotspot
from .serializers import ProductSerializer, PanoramaSerializer, HotspotSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PanoramaViewSet(viewsets.ModelViewSet):
    queryset = Panorama.objects.all()
    serializer_class = PanoramaSerializer

class HotspotViewSet(viewsets.ModelViewSet):
    queryset = Hotspot.objects.all()
    serializer_class = HotspotSerializer
