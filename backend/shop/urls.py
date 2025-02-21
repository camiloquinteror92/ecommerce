# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('panorama/<int:panorama_id>/', views.panorama_detail, name='panorama_detail'),
    path('panorama/<int:panorama_id>/define_hotspots/', views.define_hotspots, name='define_hotspots'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Carrito
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('checkout/', views.checkout, name='checkout'),
]
