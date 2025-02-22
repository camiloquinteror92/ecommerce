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
    """
    Admin para un modelo de mueble más completo.
    """
    # Campos que se muestran en la lista
    list_display = (
        'sku',
        'name',
        'final_price',
        'stock',
        'is_active',
    )
    # Campos por los que se puede filtrar en el panel lateral
    list_filter = (
        'is_active',
        'material',
        'color',
    )
    # Campos por los que se puede buscar en la parte superior
    search_fields = (
        'sku',
        'name',
        'description',
    )
    # Campos de solo lectura
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    def final_price(self, obj):
        """
        Muestra el precio final calculado 
        (discount_price si existe, de lo contrario price).
        """
        return obj.final_price
    final_price.short_description = 'Precio Final'
