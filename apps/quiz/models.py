from django.conf import settings
from django.db import models

from apps.catalog.models import Scent


class QuizQuestion(models.Model):
    text = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text


class QuizOption(models.Model):
    """An answer option. Each option nudges the quiz toward one or more
    'memory tags' (e.g. 'coastal', 'family-kitchen', 'cozy-winter') which
    are matched against tags on Scent to produce a result — this is what
    lets us recommend by nostalgic feeling rather than literal scent notes."""

    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    memory_tags = models.CharField(
        max_length=255,
        help_text="Comma-separated tags, e.g. 'coastal,summer,nostalgic-travel'"
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.question.text[:30]} → {self.text}"

    def tag_list(self):
        return [t.strip() for t in self.memory_tags.split(",") if t.strip()]


class ScentMemoryTag(models.Model):
    """Links a Scent to the memory tags it represents, so quiz answers
    (tagged the same way) can be matched to it."""
    scent = models.ForeignKey(Scent, on_delete=models.CASCADE, related_name="memory_tags")
    tag = models.SlugField(max_length=60)

    class Meta:
        unique_together = [("scent", "tag")]

    def __str__(self):
        return f"{self.scent.name}: {self.tag}"


class QuizResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="quiz_results"
    )
    session_key = models.CharField(max_length=40, blank=True)
    matched_scent = models.ForeignKey(Scent, on_delete=models.SET_NULL, null=True, related_name="quiz_matches")
    answer_tags = models.JSONField(default=list, help_text="Flattened list of memory tags collected from answers.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Result: {self.matched_scent} ({self.created_at:%Y-%m-%d})"
