"""
Business logic for subscription state transitions, kept separate from views
so it's directly unit-testable per the coding plan.
"""
from .models import Subscription, SubscriptionEvent


def pause_subscription(subscription: Subscription) -> Subscription:
    subscription.status = Subscription.Status.PAUSED
    subscription.save(update_fields=["status"])
    SubscriptionEvent.objects.create(subscription=subscription, event_type=SubscriptionEvent.EventType.PAUSED)
    return subscription


def resume_subscription(subscription: Subscription) -> Subscription:
    subscription.status = Subscription.Status.ACTIVE
    subscription.save(update_fields=["status"])
    SubscriptionEvent.objects.create(subscription=subscription, event_type=SubscriptionEvent.EventType.RESUMED)
    return subscription


def cancel_subscription(subscription: Subscription) -> Subscription:
    subscription.status = Subscription.Status.CANCELED
    subscription.save(update_fields=["status"])
    SubscriptionEvent.objects.create(subscription=subscription, event_type=SubscriptionEvent.EventType.CANCELED)
    return subscription


def swap_scent(subscription: Subscription, new_scent) -> Subscription:
    old_scent_name = subscription.current_scent.name if subscription.current_scent else "none"
    subscription.current_scent = new_scent
    subscription.save(update_fields=["current_scent"])
    SubscriptionEvent.objects.create(
        subscription=subscription,
        event_type=SubscriptionEvent.EventType.SCENT_SWAPPED,
        note=f"Swapped from {old_scent_name} to {new_scent.name}",
    )
    return subscription


def skip_next_shipment(subscription: Subscription) -> Subscription:
    SubscriptionEvent.objects.create(subscription=subscription, event_type=SubscriptionEvent.EventType.SKIPPED)
    return subscription
