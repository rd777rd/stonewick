from django.contrib import admin
from .models import Subscription, SubscriptionEvent


class SubscriptionEventInline(admin.TabularInline):
    model = SubscriptionEvent
    extra = 0
    readonly_fields = ("event_type", "note", "created_at")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "current_scent", "rotation_mode", "status")
    list_filter = ("status", "rotation_mode")
    inlines = [SubscriptionEventInline]
