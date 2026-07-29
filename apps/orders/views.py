from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from apps.catalog.models import Product
from .forms import AddressForm
from .models import Address, Order, OrderItem
from .stripe_client import create_checkout_session, construct_webhook_event


def cart_detail(request):
    return render(request, "orders/cart_detail.html", {"cart": request.cart})


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    request.cart.add(product, quantity=quantity)
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect(request.POST.get("next", "orders:cart_detail"))


def cart_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))
    request.cart.set_quantity(product, quantity)
    return redirect("orders:cart_detail")


def cart_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    request.cart.remove(product)
    return redirect("orders:cart_detail")


@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "orders/address_list.html", {"addresses": addresses})


@login_required
def address_add(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            # First address for this user becomes their default automatically.
            address.is_default = not Address.objects.filter(user=request.user).exists()
            address.save()
            messages.success(request, "Address saved.")
            next_url = request.GET.get("next") or "orders:address_list"
            return redirect(next_url)
    else:
        form = AddressForm()
    return render(request, "orders/address_form.html", {"form": form})


@login_required
def checkout(request):
    cart = request.cart
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("catalog:shop_index")

    address = Address.objects.filter(user=request.user, is_default=True).first() \
        or Address.objects.filter(user=request.user).first()
    if not address:
        messages.warning(request, "Please add a shipping address before checking out.")
        return redirect(f"{reverse('orders:address_add')}?next={reverse('orders:checkout')}")

    order = Order.objects.create(user=request.user, address=address, status=Order.Status.PENDING)
    for entry in cart:
        OrderItem.objects.create(
            order=order,
            product=entry["product"],
            product_name=entry["product"].name,
            unit_price=entry["price"],
            quantity=entry["quantity"],
        )

    success_url = request.build_absolute_uri(reverse("orders:checkout_success")) + f"?order_id={order.pk}"
    cancel_url = request.build_absolute_uri(reverse("orders:cart_detail"))

    session = create_checkout_session(
        cart, order, success_url, cancel_url, customer_email=request.user.email
    )
    order.stripe_checkout_session_id = session.id
    order.save(update_fields=["stripe_checkout_session_id"])

    return redirect(session.url, permanent=False)


@login_required
def checkout_success(request):
    order_id = request.GET.get("order_id")
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    request.cart.clear()
    return render(request, "orders/checkout_success.html", {"order": order})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = construct_webhook_event(payload, sig_header)
    except (ValueError, Exception):
        return HttpResponseBadRequest("Invalid webhook signature or payload.")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session.get("metadata", {}).get("order_id")
        if order_id:
            Order.objects.filter(pk=order_id).update(
                status=Order.Status.PAID,
                stripe_payment_intent_id=session.get("payment_intent", ""),
            )

    return HttpResponse(status=200)
