from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# Usuario personalizado con roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('manager', 'Gerente'),
        ('customer', 'Cliente'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username

# Categorías para los productos
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Producto con información extendida y relación con categoría
class Product(models.Model):
    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text="Código único de inventario (SKU)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Nombre descriptivo del producto"
    )
    description = models.TextField(
        blank=True,
        help_text="Descripción detallada del producto"
    )
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
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible en inventario"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si el producto está disponible para la venta"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        help_text="Imagen principal del producto"
    )
    material = models.CharField(
        max_length=100,
        blank=True,
        help_text="Material principal"
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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
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
        return self.discount_price if self.discount_price else self.price

# Panorama 360 con hotspots y auditoría básica
class Panorama(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Identificador único para la escena")
    image = models.ImageField("Imagen 360 (JPG)", upload_to='panoramas/')
    description = models.TextField("Descripción", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='panoramas'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Panorama, self).save(*args, **kwargs)

# Hotspot dentro de un Panorama. Puede apuntar a un Producto o a otra escena (Panorama)
class Hotspot(models.Model):
    HOTSPOT_TYPE_CHOICES = [
        ('product', 'Producto'),
        ('scene', 'Escena'),
    ]
    panorama = models.ForeignKey(
        Panorama,
        related_name='hotspots',
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=20,
        choices=HOTSPOT_TYPE_CHOICES,
        default='product'
    )
    product = models.ForeignKey(
        Product,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='hotspots'
    )
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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hotspots'
    )

    def __str__(self):
        return f"Hotspot {self.type} en {self.panorama.title}"
    
    # cart/models.py

from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart #{self.pk} - {self.user.username}"

    @property
    def total(self):
        """Suma el subtotal de todos los items del carrito."""
        return sum(item.subtotal for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        """Cantidad * precio final del producto."""
        return self.quantity * float(self.product.final_price)

