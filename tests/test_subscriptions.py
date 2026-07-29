import pytest
from decimal import Decimal

from apps.catalog.models import Product, Scent
from apps.subscriptions.models import Subscription, SubscriptionEvent
from apps.subscriptions import services


@pytest.fixture
def refill_product(db):
    return Product.objects.create(
        name="Refill Pouch", product_type=Product.ProductType.REFILL,
        description="A refill.", price=Decimal("18.00"), stock=10,
        is_subscription_eligible=True,
    )


@pytest.fixture
def scent(db):
    return Scent.objects.create(name="Beach House Morning", memory_story="Salt air.")


@pytest.fixture
def subscription(db, user, refill_product, scent):
    return Subscription.objects.create(user=user, product=refill_product, current_scent=scent)


def test_pause_sets_status_and_logs_event(subscription):
    services.pause_subscription(subscription)
    subscription.refresh_from_db()
    assert subscription.status == Subscription.Status.PAUSED
    assert subscription.events.filter(event_type=SubscriptionEvent.EventType.PAUSED).exists()


def test_resume_sets_status_active(subscription):
    services.pause_subscription(subscription)
    services.resume_subscription(subscription)
    subscription.refresh_from_db()
    assert subscription.status == Subscription.Status.ACTIVE


def test_cancel_sets_status_canceled(subscription):
    services.cancel_subscription(subscription)
    subscription.refresh_from_db()
    assert subscription.status == Subscription.Status.CANCELED


def test_swap_scent_updates_current_scent_and_logs_event(subscription, db):
    new_scent = Scent.objects.create(name="Grandma's Kitchen", memory_story="Cinnamon.")
    services.swap_scent(subscription, new_scent)
    subscription.refresh_from_db()
    assert subscription.current_scent == new_scent
    event = subscription.events.filter(event_type=SubscriptionEvent.EventType.SCENT_SWAPPED).first()
    assert event is not None
    assert "Grandma's Kitchen" in event.note


def test_skip_next_shipment_logs_event_without_changing_status(subscription):
    services.skip_next_shipment(subscription)
    subscription.refresh_from_db()
    assert subscription.status == Subscription.Status.ACTIVE
    assert subscription.events.filter(event_type=SubscriptionEvent.EventType.SKIPPED).exists()
