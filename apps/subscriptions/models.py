from django.conf import settings
from django.db import models

from apps.catalog.models import Product, Scent


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        CANCELED = "canceled", "Canceled"

    class RotationMode(models.TextChoices):
        SEASONAL = "seasonal", "Rotate with the seasons"
        FIXED = "fixed", "Always the same scent"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="subscriptions")
    current_scent = models.ForeignKey(Scent, on_delete=models.SET_NULL, null=True, related_name="+")
    rotation_mode = models.CharField(max_length=10, choices=RotationMode.choices, default=RotationMode.SEASONAL)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.product.name} ({self.status})"


class SubscriptionEvent(models.Model):
    class EventType(models.TextChoices):
        PAUSED = "paused", "Paused"
        RESUMED = "resumed", "Resumed"
        SKIPPED = "skipped", "Skipped a shipment"
        SCENT_SWAPPED = "scent_swapped", "Scent swapped"
        CANCELED = "canceled", "Canceled"

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subscription} — {self.event_type}"
