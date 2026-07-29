from .cart import Cart


class CartMiddleware:
    """Attaches request.cart so views/templates can access it without
    re-instantiating the Cart helper each time."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.cart = Cart(request)
        return self.get_response(request)
