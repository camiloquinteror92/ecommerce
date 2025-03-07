# Generated by Django 5.1.6 on 2025-02-28 13:21

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('manager', 'Gerente'), ('customer', 'Cliente')], default='customer', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Panorama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(help_text='Identificador único para la escena', unique=True)),
                ('image', models.ImageField(upload_to='panoramas/', verbose_name='Imagen 360 (JPG)')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='panoramas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(help_text='Código único de inventario (SKU)', max_length=50, unique=True)),
                ('name', models.CharField(help_text='Nombre descriptivo del producto', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Descripción detallada del producto')),
                ('price', models.DecimalField(decimal_places=2, help_text='Precio de venta', max_digits=10)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, help_text='Precio con descuento (opcional)', max_digits=10, null=True)),
                ('stock', models.PositiveIntegerField(default=0, help_text='Cantidad disponible en inventario')),
                ('is_active', models.BooleanField(default=True, help_text='Indica si el producto está disponible para la venta')),
                ('image', models.ImageField(blank=True, help_text='Imagen principal del producto', null=True, upload_to='products/')),
                ('material', models.CharField(blank=True, help_text='Material principal', max_length=100)),
                ('color', models.CharField(blank=True, help_text='Color o acabado principal', max_length=50)),
                ('width', models.DecimalField(blank=True, decimal_places=2, help_text='Ancho (cm)', max_digits=6, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, help_text='Altura (cm)', max_digits=6, null=True)),
                ('depth', models.DecimalField(blank=True, decimal_places=2, help_text='Profundidad (cm)', max_digits=6, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Fecha de creación del registro')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Fecha de la última actualización')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.category')),
            ],
        ),
        migrations.CreateModel(
            name='Hotspot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('product', 'Producto'), ('scene', 'Escena')], default='product', max_length=20)),
                ('x', models.FloatField(help_text='Valor entre 0 y 100', verbose_name='Coordenada X')),
                ('y', models.FloatField(help_text='Valor entre 0 y 100', verbose_name='Coordenada Y')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Descripción del Hotspot')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hotspots', to=settings.AUTH_USER_MODEL)),
                ('connected_panorama', models.ForeignKey(blank=True, help_text="Panorama al que se navega si el hotspot es de tipo 'scene'.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incoming_hotspots', to='shop.panorama')),
                ('panorama', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotspots', to='shop.panorama')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hotspots', to='shop.product')),
            ],
        ),
    ]
