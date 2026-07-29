import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("meta_title", models.CharField(blank=True, help_text="Shown in search results and browser tabs. Falls back to the object's name/title if left blank. Aim for under 60 characters.", max_length=70)),
                ("meta_description", models.CharField(blank=True, help_text="Shown as the snippet in search results. Falls back to a truncated description if left blank. Aim for under 155 characters.", max_length=160)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=110, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name_plural": "categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Scent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=110, unique=True)),
                ("memory_story", models.TextField(help_text="Narrative description framed as a nostalgic memory, e.g. 'The screen door slamming at grandma's lake house...' rather than generic notes like 'vanilla, cedar'.")),
                ("supporting_notes", models.CharField(blank=True, help_text="Optional literal notes for customers who want them, e.g. 'vanilla, driftwood, sea salt'.", max_length=255)),
                ("season", models.CharField(choices=[("spring", "Spring"), ("summer", "Summer"), ("autumn", "Autumn"), ("winter", "Winter"), ("year_round", "Year-round")], default="year_round", max_length=20)),
                ("image", models.ImageField(blank=True, null=True, upload_to="scents/")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("meta_title", models.CharField(blank=True, help_text="Shown in search results and browser tabs. Falls back to the object's name/title if left blank. Aim for under 60 characters.", max_length=70)),
                ("meta_description", models.CharField(blank=True, help_text="Shown as the snippet in search results. Falls back to a truncated description if left blank. Aim for under 155 characters.", max_length=160)),
                ("name", models.CharField(max_length=150)),
                ("slug", models.SlugField(blank=True, max_length=170, unique=True)),
                ("product_type", models.CharField(choices=[("vessel", "Vessel"), ("refill", "Refill"), ("bundle", "Starter Bundle")], max_length=10)),
                ("vessel_material", models.CharField(choices=[("stone", "Stone"), ("ceramic", "Ceramic"), ("na", "N/A")], default="na", max_length=10)),
                ("description", models.TextField()),
                ("care_instructions", models.TextField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("is_subscription_eligible", models.BooleanField(default=False, help_text="Refills eligible for the seasonal rotation subscription.")),
                ("stripe_price_id", models.CharField(blank=True, help_text="Stripe Price ID (one-time). For subscription-eligible refills, also set the recurring Stripe Price ID below.", max_length=100)),
                ("stripe_subscription_price_id", models.CharField(blank=True, max_length=100)),
                ("stock", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="products", to="catalog.category")),
                ("scent", models.ForeignKey(blank=True, help_text="Leave blank for unscented vessels.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="products", to="catalog.scent")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="products/")),
                ("alt_text", models.CharField(help_text="Descriptive alt text for SEO/accessibility, e.g. 'terracotta ceramic refillable candle vessel on linen'.", max_length=200)),
                ("is_primary", models.BooleanField(default=False)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="catalog.product")),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]
