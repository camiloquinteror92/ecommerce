# shop/api/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet, PanoramaViewSet, HotspotViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'panoramas', PanoramaViewSet, basename='panorama')
router.register(r'hotspots', HotspotViewSet, basename='hotspot')

urlpatterns = [
    path('', include(router.urls)),
]
