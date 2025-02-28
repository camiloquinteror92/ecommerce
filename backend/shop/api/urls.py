from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.api.views.product_views import ProductViewSet
from shop.api.views.panorama_views import PanoramaViewSet
from shop.api.views.hotspot_views import HotspotViewSet
from shop.api.views.auth_views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.cart_views import CartViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'panoramas', PanoramaViewSet, basename='panorama')
router.register(r'hotspots', HotspotViewSet, basename='hotspot')
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
