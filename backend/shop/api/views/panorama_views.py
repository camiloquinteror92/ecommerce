# backend/shop/api/views/panorama_views.py
from rest_framework import viewsets
from shop.models import Panorama
from shop.api.serializers.panorama_serializers import PanoramaSerializer
from shop.api.permissions import IsAdminOrManagerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class PanoramaViewSet(viewsets.ModelViewSet):
    queryset = Panorama.objects.all()
    serializer_class = PanoramaSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']
