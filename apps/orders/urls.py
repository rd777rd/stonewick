from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("addresses/", views.address_list, name="address_list"),
    path("addresses/add/", views.address_add, name="address_add"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
]
