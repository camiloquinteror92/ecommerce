from django.contrib import admin
from .models import Product, Panorama, Hotspot

class HotspotInline(admin.TabularInline):
    model = Hotspot
    fk_name = 'panorama'  # Indica que 'panorama' es la FK principal para el inline
    extra = 1

@admin.register(Panorama)
class PanoramaAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    inlines = [HotspotInline]

@admin.register(Hotspot)
class HotspotAdmin(admin.ModelAdmin):
    list_display = ('panorama', 'type', 'x', 'y')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
