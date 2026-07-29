from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    favorite_scent_memory = models.CharField(
        max_length=255, blank=True,
        help_text="Freeform note on what memory/feeling they're chasing, captured post-quiz."
    )

    def __str__(self):
        return f"Profile: {self.user}"
