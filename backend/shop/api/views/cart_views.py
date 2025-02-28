# cart/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from shop.models import Cart, CartItem
from ..serializers.cart_serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet que maneja:
    - GET /carts/ -> lista de carritos activos del usuario
    - POST /carts/ -> crea un carrito
    - GET /carts/<id>/ -> detalle de un carrito
    - POST /carts/<id>/add_item/
    - POST /carts/<id>/remove_item/
    - POST /carts/<id>/clear/
    - POST /carts/<id>/checkout/
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra los carritos activos pertenecientes al usuario actual
        return Cart.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        # Al crear un carrito, se asigna el usuario automáticamente
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """
        POST /carts/<pk>/add_item/
        {
            "product_id": <int>,
            "quantity": <int>
        }
        Agrega (o incrementa) la cantidad de un producto en el carrito.
        """
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id
        )
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """
        POST /carts/<pk>/remove_item/
        {
            "product_id": <int>
        }
        Elimina el producto indicado del carrito.
        """
        cart = self.get_object()
        product_id = request.data.get('product_id')

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
        except CartItem.DoesNotExist:
            pass

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """
        POST /carts/<pk>/clear/
        Elimina todos los items del carrito.
        """
        cart = self.get_object()
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        """
        POST /carts/<pk>/checkout/
        Marca el carrito como inactivo y simula el fin de la compra.
        """
        cart = self.get_object()
        # Aquí podrías crear una "Order", procesar pagos, etc.
        cart.is_active = False
        cart.save()
        return Response(
            {'message': 'Carrito finalizado. Orden creada (simulada).'},
            status=status.HTTP_200_OK
        )
