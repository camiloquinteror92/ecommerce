def cart_item_count(request):
    cart = request.session.get('cart', {})
    total_items = 0
    for product_id, details in cart.items():
        total_items += details['quantity']
    return {
        'cart_item_count': total_items
    }
