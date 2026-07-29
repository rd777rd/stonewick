"""Thin wrapper around the Stripe SDK so views stay simple and testable."""
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(cart, order, success_url, cancel_url, customer_email=None):
    line_items = []
    for entry in cart:
        product = entry["product"]
        if product.stripe_price_id:
            line_items.append({"price": product.stripe_price_id, "quantity": entry["quantity"]})
        else:
            # Fallback: build an ad-hoc price so checkout still works even if
            # a Stripe Price ID hasn't been configured yet for this product.
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product.name},
                    "unit_amount": int(product.price * 100),
                },
                "quantity": entry["quantity"],
            })

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=customer_email,
        metadata={"order_id": str(order.pk)},
    )
    return session


def create_subscription_checkout_session(product, success_url, cancel_url, customer_email=None):
    """Used by the subscriptions app when a customer starts a recurring refill plan."""
    price_id = product.stripe_subscription_price_id
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=customer_email,
        metadata={"product_id": str(product.pk)},
    )
    return session


def construct_webhook_event(payload, sig_header):
    return stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
