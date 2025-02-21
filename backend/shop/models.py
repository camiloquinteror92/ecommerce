from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


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
