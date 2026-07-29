from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.shop_index, name="shop_index"),
    path("vessels/", views.vessel_list, name="vessel_list"),
    path("refills/", views.refill_list, name="refill_list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
]
