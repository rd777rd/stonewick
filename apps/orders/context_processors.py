def cart(request):
    cart_obj = getattr(request, "cart", None)
    return {
        "cart_item_count": len(cart_obj) if cart_obj else 0,
    }
