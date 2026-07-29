"""
Session-based cart. Kept intentionally simple (no DB persistence required
until checkout) — appropriate for MVP traffic levels per the scaling plan.
"""
from decimal import Decimal

from apps.catalog.models import Product

CART_SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.pk)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += quantity
        else:
            self.cart[product_id] = {"quantity": quantity, "price": str(product.price)}
        self.save()

    def remove(self, product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def set_quantity(self, product, quantity):
        product_id = str(product.pk)
        if product_id in self.cart:
            if quantity <= 0:
                self.remove(product)
            else:
                self.cart[product_id]["quantity"] = quantity
                self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.cart = {}
        self.session[CART_SESSION_KEY] = self.cart
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        products_by_id = {str(p.pk): p for p in products}
        for product_id, item in self.cart.items():
            product = products_by_id.get(product_id)
            if not product:
                continue
            price = Decimal(item["price"])
            quantity = item["quantity"]
            yield {
                "product": product,
                "price": price,
                "quantity": quantity,
                "line_total": price * quantity,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    @property
    def total(self):
        return sum((entry["line_total"] for entry in self), Decimal("0.00"))
