from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import SEOFields


class Category(SEOFields):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:category_detail", args=[self.slug])


class Scent(models.Model):
    """A scent is the fragrance itself — separate from the physical product,
    since one scent may be sold as a vessel-scented-sample, a refill pouch,
    and referenced by the Scent Memory Quiz results."""

    class Season(models.TextChoices):
        SPRING = "spring", "Spring"
        SUMMER = "summer", "Summer"
        AUTUMN = "autumn", "Autumn"
        WINTER = "winter", "Winter"
        YEAR_ROUND = "year_round", "Year-round"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    memory_story = models.TextField(
        help_text="Narrative description framed as a nostalgic memory, "
                   "e.g. 'The screen door slamming at grandma's lake house...' "
                   "rather than generic notes like 'vanilla, cedar'."
    )
    supporting_notes = models.CharField(
        max_length=255, blank=True,
        help_text="Optional literal notes for customers who want them, e.g. 'vanilla, driftwood, sea salt'."
    )
    season = models.CharField(max_length=20, choices=Season.choices, default=Season.YEAR_ROUND)
    image = models.ImageField(upload_to="scents/", blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(SEOFields):
    class ProductType(models.TextChoices):
        VESSEL = "vessel", "Vessel"
        REFILL = "refill", "Refill"
        BUNDLE = "bundle", "Starter Bundle"

    class VesselMaterial(models.TextChoices):
        STONE = "stone", "Stone"
        CERAMIC = "ceramic", "Ceramic"
        NA = "na", "N/A"

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    product_type = models.CharField(max_length=10, choices=ProductType.choices)
    scent = models.ForeignKey(
        Scent, on_delete=models.SET_NULL, null=True, blank=True, related_name="products",
        help_text="Leave blank for unscented vessels."
    )
    vessel_material = models.CharField(max_length=10, choices=VesselMaterial.choices, default=VesselMaterial.NA)
    description = models.TextField()
    care_instructions = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_subscription_eligible = models.BooleanField(
        default=False, help_text="Refills eligible for the seasonal rotation subscription."
    )
    stripe_price_id = models.CharField(
        max_length=100, blank=True,
        help_text="Stripe Price ID (one-time). For subscription-eligible refills, "
                   "also set the recurring Stripe Price ID below."
    )
    stripe_subscription_price_id = models.CharField(max_length=100, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            self.slug = base
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.slug])

    @property
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(
        max_length=200,
        help_text="Descriptive alt text for SEO/accessibility, e.g. "
                   "'terracotta ceramic refillable candle vessel on linen'."
    )
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.product.name}"
