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
            name="QuizQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=255)),
                ("order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="ScentMemoryTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tag", models.SlugField(max_length=60)),
                ("scent", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memory_tags", to="catalog.scent")),
            ],
            options={
                "unique_together": {("scent", "tag")},
            },
        ),
        migrations.CreateModel(
            name="QuizResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(blank=True, max_length=40)),
                ("answer_tags", models.JSONField(default=list, help_text="Flattened list of memory tags collected from answers.")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("matched_scent", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="quiz_matches", to="catalog.scent")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="quiz_results", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="QuizOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=255)),
                ("memory_tags", models.CharField(help_text="Comma-separated tags, e.g. 'coastal,summer,nostalgic-travel'", max_length=255)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="quiz.quizquestion")),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]
