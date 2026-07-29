from django.contrib import admin
from .models import Category, Scent, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Scent)
class ScentAdmin(admin.ModelAdmin):
    list_display = ("name", "season", "slug")
    list_filter = ("season",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_type", "category", "scent", "price", "stock", "is_active")
    list_filter = ("product_type", "category", "is_active", "is_subscription_eligible")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "product_type", "scent", "vessel_material")}),
        ("Details", {"fields": ("description", "care_instructions", "price", "stock", "is_active")}),
        ("Subscriptions", {"fields": ("is_subscription_eligible", "stripe_price_id", "stripe_subscription_price_id")}),
        ("SEO", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )
