import pytest
from decimal import Decimal
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from apps.catalog.models import Product
from apps.orders.cart import Cart


@pytest.fixture
def request_with_session(db):
    factory = RequestFactory()
    request = factory.get("/")
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.fixture
def vessel(db):
    return Product.objects.create(
        name="Ceramic Vessel", product_type=Product.ProductType.VESSEL,
        description="A vessel.", price=Decimal("48.00"), stock=10,
    )


@pytest.fixture
def refill(db):
    return Product.objects.create(
        name="Refill Pouch", product_type=Product.ProductType.REFILL,
        description="A refill.", price=Decimal("18.00"), stock=10,
    )


def test_add_single_item_computes_correct_total(request_with_session, vessel):
    cart = Cart(request_with_session)
    cart.add(vessel, quantity=1)
    assert cart.total == Decimal("48.00")
    assert len(cart) == 1


def test_add_multiple_quantities_and_items(request_with_session, vessel, refill):
    cart = Cart(request_with_session)
    cart.add(vessel, quantity=2)
    cart.add(refill, quantity=3)
    assert cart.total == Decimal("48.00") * 2 + Decimal("18.00") * 3
    assert len(cart) == 5


def test_set_quantity_to_zero_removes_item(request_with_session, vessel):
    cart = Cart(request_with_session)
    cart.add(vessel, quantity=1)
    cart.set_quantity(vessel, 0)
    assert len(cart) == 0
    assert cart.total == Decimal("0.00")


def test_remove_item(request_with_session, vessel, refill):
    cart = Cart(request_with_session)
    cart.add(vessel, quantity=1)
    cart.add(refill, quantity=1)
    cart.remove(vessel)
    assert len(cart) == 1
    assert cart.total == Decimal("18.00")


def test_clear_empties_cart(request_with_session, vessel):
    cart = Cart(request_with_session)
    cart.add(vessel, quantity=2)
    cart.clear()
    assert len(cart) == 0
