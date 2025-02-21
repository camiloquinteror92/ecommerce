# shop/views.py
import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Panorama, Hotspot, Product

# ========== 1) VISTAS DE PANORAMAS 360 ==========

def home(request):
    """
    Muestra la lista de todos los panoramas disponibles.
    """
    panoramas = Panorama.objects.all()
    return render(request, 'shop/home.html', {'panoramas': panoramas})

def panorama_detail(request, panorama_id):
    """
    Muestra un visor 360 con Pannellum que incluye TODAS las escenas (Panorama)
    para poder saltar entre ellas, pero arranca en la que corresponde a panorama_id.
    
    - Si un Hotspot es de tipo 'scene', enlaza a otro Panorama (connected_panorama).
    - Si es de tipo 'product', muestra info de producto (ya sea con clickHandlerFunc
      o createTooltipFunc para tooltips).
    """
    # Panorama de inicio
    start_panorama = get_object_or_404(Panorama, pk=panorama_id)
    # Cargamos todos los panoramas para construir un "tour" multi-escena
    all_panoramas = Panorama.objects.prefetch_related('hotspots').all()

    # Config base de Pannellum
    pannellum_config = {
        "default": {
            "firstScene": start_panorama.slug,
            "author": "Tu E-commerce",
            "autoLoad": True,
            "hfov": 120  # Ajusta para alejar/acercar la vista
        },
        "scenes": {}
    }

    # Para cada panorama, construimos la entrada en 'scenes'
    for pano in all_panoramas:
        pano_hotspots = []
        for hs in pano.hotspots.all():
            # Convertimos x,y (porcentaje) a yaw,pitch
            yaw = (hs.x * 360.0 / 100.0) - 180.0
            pitch = 90.0 - (hs.y * 180.0 / 100.0)

            if hs.type == 'scene' and hs.connected_panorama:
                # Hotspot para saltar a otra escena
                pano_hotspots.append({
                    "pitch": pitch,
                    "yaw": yaw,
                    "type": "scene",
                    "text": hs.description or hs.connected_panorama.title,
                    "sceneId": hs.connected_panorama.slug
                })
            elif hs.type == 'product' and hs.product:
                # Hotspot que muestra info de producto (puede ser con tooltip o click)
                pano_hotspots.append({
                    "pitch": pitch,
                    "yaw": yaw,
                    "type": "info",
                    "text": hs.description or hs.product.name,
                    # Ejemplo con clickHandlerFunc (redirige al producto):
                    # "clickHandlerFunc": "showProductInfo",
                    # "clickHandlerArgs": {"productId": hs.product.id}

                    # Ejemplo con createTooltipFunc (tooltip al hover):
                    "createTooltipFunc": "createProductTooltip",
                    "createTooltipArgs": {
                        "productId": hs.product.id,
                        "name": hs.product.name,
                        "price": str(hs.product.price),
                        "image": hs.product.image.url
                    }
                })
            # Otros casos se omiten

        pannellum_config["scenes"][pano.slug] = {
            "title": pano.title,
            "panorama": pano.image.url,
            "hotSpots": pano_hotspots
        }

    config_json = json.dumps(pannellum_config)

    return render(request, 'shop/panorama_detail.html', {
        "start_panorama": start_panorama,
        "config_json": config_json
    })

def define_hotspots(request, panorama_id):
    """
    Define hotspots de forma manual sobre una imagen estática (capturando x,y en %).
    """
    panorama = get_object_or_404(Panorama, pk=panorama_id)

    if request.method == "POST":
        # Recibimos los hotspots en formato JSON
        hotspots_data = json.loads(request.POST.get('hotspots', '[]'))
        for h in hotspots_data:
            hs_type = h.get('type', 'product')
            new_hs = Hotspot.objects.create(
                panorama=panorama,
                type=hs_type,
                x=h['x'],
                y=h['y'],
                description=h.get('description', '')
            )

            # Si es un hotspot de producto
            if hs_type == 'product' and h.get('product_id'):
                product = get_object_or_404(Product, pk=h['product_id'])
                new_hs.product = product
                new_hs.save()
            # Si es un hotspot de escena
            elif hs_type == 'scene' and h.get('connected_panorama_id'):
                linked_pano = get_object_or_404(Panorama, pk=h['connected_panorama_id'])
                new_hs.connected_panorama = linked_pano
                new_hs.save()

        return redirect('panorama_detail', panorama_id=panorama.id)

    # Listamos todos los panoramas y productos para elegirlos
    all_panoramas = Panorama.objects.all()
    all_products = Product.objects.all()

    return render(request, 'shop/define_hotspots.html', {
        "panorama": panorama,
        "all_panoramas": all_panoramas,
        "all_products": all_products
    })

def product_detail(request, product_id):
    """
    Muestra la ficha de un producto (imagen, descripción, precio),
    con un formulario para agregarlo al carrito.
    """
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {
        "product": product
    })


# ========== 2) VISTAS DEL CARRITO DE COMPRAS ==========

def cart_detail(request):
    """
    Muestra los productos en el carrito, la cantidad de cada uno y el total.
    """
    cart = request.session.get('cart', {})
    total = 0
    items = []

    # Construimos una lista de items para la plantilla
    for product_id, details in cart.items():
        subtotal = float(details['price']) * details['quantity']
        total += subtotal
        items.append({
            'product_id': product_id,
            'name': details['name'],
            'price': details['price'],
            'quantity': details['quantity'],
            'image': details['image'],
            'subtotal': subtotal
        })

    return render(request, 'shop/cart_detail.html', {
        'cart_items': items,
        'total': total
    })

def cart_add(request, product_id):
    """
    Agrega un producto al carrito (o aumenta la cantidad si ya existe).
    Se espera que en product_detail.html haya un formulario con la cantidad deseada.
    """
    product = get_object_or_404(Product, pk=product_id)
    quantity = request.GET.get('quantity') or request.POST.get('quantity') or '1'
    quantity = int(quantity)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': quantity,
            'image': product.image.url
        }

    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_remove(request, product_id):
    """
    Elimina por completo un producto del carrito.
    """
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_clear(request):
    """
    Vacía por completo el carrito de la sesión.
    """
    request.session['cart'] = {}
    return redirect('cart_detail')

def checkout(request):
    """
    Muestra el resumen final del carrito y, en un caso real,
    procesaría el pago y crearía una orden en la base de datos.
    """
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    total = 0
    for details in cart.values():
        total += float(details['price']) * details['quantity']

    if request.method == 'POST':
        # Aquí podrías procesar el pago, crear una orden, etc.
        # Por ahora, simulamos y vaciamos el carrito:
        request.session['cart'] = {}
        return render(request, 'shop/checkout_success.html')

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'total': total
    })
