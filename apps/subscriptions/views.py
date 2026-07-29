from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from apps.catalog.models import Scent
from .models import Subscription
from . import services


@login_required
def manage(request):
    subscriptions = Subscription.objects.filter(user=request.user).select_related("product", "current_scent")
    return render(request, "subscriptions/manage.html", {"subscriptions": subscriptions})


@login_required
def pause(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    services.pause_subscription(sub)
    messages.success(request, "Subscription paused.")
    return redirect("subscriptions:manage")


@login_required
def resume(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    services.resume_subscription(sub)
    messages.success(request, "Subscription resumed.")
    return redirect("subscriptions:manage")


@login_required
def skip(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    services.skip_next_shipment(sub)
    messages.success(request, "Next shipment skipped.")
    return redirect("subscriptions:manage")


@login_required
def swap_scent(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == "POST":
        scent = get_object_or_404(Scent, pk=request.POST.get("scent_id"))
        services.swap_scent(sub, scent)
        messages.success(request, f"Your subscription is now set to {scent.name}.")
        return redirect("subscriptions:manage")
    scents = Scent.objects.all()
    return render(request, "subscriptions/swap_scent.html", {"subscription": sub, "scents": scents})


@login_required
def cancel(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == "POST":
        services.cancel_subscription(sub)
        messages.success(request, "Subscription canceled.")
        return redirect("subscriptions:manage")
    return render(request, "subscriptions/cancel_confirm.html", {"subscription": sub})
