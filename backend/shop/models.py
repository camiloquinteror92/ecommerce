from django.db import models

from django.db import models
from django.utils import timezone

class Product(models.Model):
    """
    Modelo de producto para una tienda de muebles.
    Incluye campos de inventario, dimensiones, material, etc.
    """
    # Identificación y datos básicos
    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text="Código único de inventario (SKU)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Nombre descriptivo del mueble"
    )
    description = models.TextField(
        blank=True,
        help_text="Descripción detallada del producto"
    )
    
    # Precios y descuentos
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio de venta"
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Precio con descuento (opcional)"
    )

    # Inventario y estado
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible en inventario"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si el producto está disponible para la venta"
    )

    # Información visual
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        help_text="Imagen principal del producto"
    )

    # Datos específicos de muebles
    material = models.CharField(
        max_length=100,
        blank=True,
        help_text="Material principal (madera, metal, etc.)"
    )
    color = models.CharField(
        max_length=50,
        blank=True,
        help_text="Color o acabado principal"
    )
    width = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Ancho (cm)"
    )
    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Altura (cm)"
    )
    depth = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Profundidad (cm)"
    )

    # Metadatos de creación y actualización
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del registro"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de la última actualización"
    )

    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"

    @property
    def final_price(self):
        """
        Retorna el precio con descuento si está definido, 
        de lo contrario el precio normal.
        """
        return self.discount_price if self.discount_price else self.price



class Panorama(models.Model):
    """
    Representa una imagen 360 equirectangular (JPG).
    'slug' se usará para identificarla en Pannellum.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Identificador único para la escena")
    image = models.ImageField("Imagen 360 (JPG)", upload_to='panoramas/')
    description = models.TextField("Descripción", blank=True)

    def __str__(self):
        return self.title


class Hotspot(models.Model):
    """
    Un punto interactivo dentro de un Panorama.
    Puede apuntar a un Product (type='product') o a otro Panorama (type='scene').
    Se almacenan x e y en porcentaje (0-100), como en tu MVP original.
    """
    HOTSPOT_TYPE_CHOICES = [
        ('product', 'Producto'),
        ('scene', 'Escena'),
    ]
    panorama = models.ForeignKey(Panorama, related_name='hotspots', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=HOTSPOT_TYPE_CHOICES, default='product')
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)
    # Si el hotspot apunta a otra escena (cambiar de panorama)
    connected_panorama = models.ForeignKey(
        Panorama,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='incoming_hotspots',
        help_text="Panorama al que se navega si el hotspot es de tipo 'scene'."
    )
    x = models.FloatField("Coordenada X", help_text="Valor entre 0 y 100")
    y = models.FloatField("Coordenada Y", help_text="Valor entre 0 y 100")
    description = models.CharField("Descripción del Hotspot", max_length=255, blank=True)

    def __str__(self):
        return f"Hotspot {self.type} en {self.panorama.title}"
