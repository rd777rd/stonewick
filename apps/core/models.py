from django.db import models


class SEOFields(models.Model):
    """
    Abstract mixin providing per-object SEO metadata. Reused by Product,
    Category, and Post so every content-bearing page can have a unique,
    editable title/description without a developer touching code.
    """
    meta_title = models.CharField(
        max_length=70, blank=True,
        help_text="Shown in search results and browser tabs. Falls back to the "
                   "object's name/title if left blank. Aim for under 60 characters.",
    )
    meta_description = models.CharField(
        max_length=160, blank=True,
        help_text="Shown as the snippet in search results. Falls back to a "
                   "truncated description if left blank. Aim for under 155 characters.",
    )

    class Meta:
        abstract = True

    def get_meta_title(self, fallback: str) -> str:
        return self.meta_title or fallback

    def get_meta_description(self, fallback: str) -> str:
        return self.meta_description or fallback


class ContactMessage(models.Model):
    """Stores submissions from the /contact/ page."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> - {self.created_at:%Y-%m-%d}"
