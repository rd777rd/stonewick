from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Product, Category


def shop_index(request):
    return render(request, "catalog/shop_index.html")


def vessel_list(request):
    products = Product.objects.filter(product_type=Product.ProductType.VESSEL, is_active=True)
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "catalog/product_list.html", {
        "page_obj": page_obj,
        "heading": "Vessels",
        "canonical_path": "/shop/vessels/",
    })


def refill_list(request):
    products = Product.objects.filter(product_type=Product.ProductType.REFILL, is_active=True)
    season = request.GET.get("season")
    if season:
        products = products.filter(scent__season=season)
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "catalog/product_list.html", {
        "page_obj": page_obj,
        "heading": "Refills",
        "canonical_path": "/shop/refills/",
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    crumbs = [("Home", reverse("core:home")), ("Shop", reverse("catalog:shop_index")), (category.name, None)]
    return render(request, "catalog/category_detail.html", {
        "category": category,
        "page_obj": page_obj,
        "crumbs": crumbs,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category", "scent").prefetch_related("images"),
        slug=slug, is_active=True,
    )
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    crumbs = [("Home", reverse("core:home")), ("Shop", reverse("catalog:shop_index"))]
    if product.category:
        crumbs.append((product.category.name, product.category.get_absolute_url()))
    crumbs.append((product.name, None))

    return render(request, "catalog/product_detail.html", {
        "product": product,
        "related": related,
        "crumbs": crumbs,
    })
