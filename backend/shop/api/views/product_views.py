# backend/shop/api/views/product_views.py
from rest_framework import viewsets
from shop.models import Product
from shop.api.serializers.product_serializers import ProductSerializer
from shop.api.permissions import IsAdminOrManagerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_active', 'material', 'color']
