import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rotation_mode", models.CharField(choices=[("seasonal", "Rotate with the seasons"), ("fixed", "Always the same scent")], default="seasonal", max_length=10)),
                ("status", models.CharField(choices=[("active", "Active"), ("paused", "Paused"), ("canceled", "Canceled")], default="active", max_length=10)),
                ("stripe_subscription_id", models.CharField(blank=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("current_scent", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="catalog.scent")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subscriptions", to="catalog.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subscriptions", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="SubscriptionEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_type", models.CharField(choices=[("paused", "Paused"), ("resumed", "Resumed"), ("skipped", "Skipped a shipment"), ("scent_swapped", "Scent swapped"), ("canceled", "Canceled")], max_length=20)),
                ("note", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("subscription", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="subscriptions.subscription")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
