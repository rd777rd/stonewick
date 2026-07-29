import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PostCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=110, unique=True)),
            ],
            options={
                "verbose_name_plural": "post categories",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("meta_title", models.CharField(blank=True, help_text="Shown in search results and browser tabs. Falls back to the object's name/title if left blank. Aim for under 60 characters.", max_length=70)),
                ("meta_description", models.CharField(blank=True, help_text="Shown as the snippet in search results. Falls back to a truncated description if left blank. Aim for under 155 characters.", max_length=160)),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, max_length=220, unique=True)),
                ("excerpt", models.CharField(blank=True, max_length=300)),
                ("body", models.TextField()),
                ("cover_image", models.ImageField(blank=True, null=True, upload_to="journal/")),
                ("is_published", models.BooleanField(default=True)),
                ("published_at", models.DateTimeField(auto_now_add=True)),
                ("author", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="posts", to="journal.postcategory")),
            ],
            options={
                "ordering": ["-published_at"],
            },
        ),
    ]
