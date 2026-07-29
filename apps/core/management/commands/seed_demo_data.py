"""
Seeds minimal demo data so a fresh clone is immediately explorable:
a category, two scents (each tagged for the quiz), a vessel, and a
subscription-eligible refill. Safe to run multiple times (get_or_create).

Usage: python manage.py seed_demo_data
"""
from django.core.management.base import BaseCommand

from apps.catalog.models import Category, Scent, Product
from apps.quiz.models import QuizQuestion, QuizOption, ScentMemoryTag


class Command(BaseCommand):
    help = "Seed minimal demo data for local development."

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(
            name="Coastal Collection",
            defaults={"description": "Scents inspired by seaside memories."},
        )

        beach_house, _ = Scent.objects.get_or_create(
            name="Beach House Morning",
            defaults={
                "memory_story": "The screen door slamming, salt air drifting in through an open "
                                 "window, and coffee brewing before anyone else is awake.",
                "supporting_notes": "sea salt, driftwood, white tea",
                "season": Scent.Season.SUMMER,
            },
        )
        grandmas_kitchen, _ = Scent.objects.get_or_create(
            name="Grandma's Kitchen",
            defaults={
                "memory_story": "Cinnamon rolls cooling on the counter and the low hum of the "
                                 "radio on a Sunday afternoon.",
                "supporting_notes": "cinnamon, vanilla, warm butter",
                "season": Scent.Season.WINTER,
            },
        )

        for tag in ["coastal", "summer", "nostalgic-travel"]:
            ScentMemoryTag.objects.get_or_create(scent=beach_house, tag=tag)
        for tag in ["family-kitchen", "cozy-winter", "nostalgic-home"]:
            ScentMemoryTag.objects.get_or_create(scent=grandmas_kitchen, tag=tag)

        Product.objects.get_or_create(
            name="Ceramic Reed Diffuser Vessel",
            defaults={
                "category": category,
                "product_type": Product.ProductType.VESSEL,
                "vessel_material": Product.VesselMaterial.CERAMIC,
                "description": "A hand-finished ceramic vessel designed for a lifetime of refills.",
                "care_instructions": "Wipe clean with a damp cloth. Avoid submerging in water.",
                "price": "48.00",
                "stock": 25,
            },
        )
        Product.objects.get_or_create(
            name="Beach House Morning Refill Pouch",
            defaults={
                "category": category,
                "product_type": Product.ProductType.REFILL,
                "scent": beach_house,
                "description": "A compostable refill pouch, ready in seconds — no wax pouring required.",
                "price": "18.00",
                "stock": 100,
                "is_subscription_eligible": True,
            },
        )

        q1, _ = QuizQuestion.objects.get_or_create(text="Where do you feel most at peace?", order=1)
        QuizOption.objects.get_or_create(question=q1, text="Somewhere near the ocean", defaults={
            "memory_tags": "coastal,summer,nostalgic-travel", "order": 1,
        })
        QuizOption.objects.get_or_create(question=q1, text="In a cozy kitchen full of family", defaults={
            "memory_tags": "family-kitchen,cozy-winter,nostalgic-home", "order": 2,
        })

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
