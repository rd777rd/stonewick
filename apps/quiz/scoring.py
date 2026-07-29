"""
Scent Memory Quiz scoring logic.

Each answer contributes a set of "memory tags" (e.g. 'coastal', 'cozy-winter').
We tally tag frequency across all submitted answers, then find the Scent
whose own memory tags overlap most with the user's tally. Ties are broken
by preferring a scent matching the current real-world season, then by
scent name for full determinism (important for testability).
"""
from collections import Counter

from apps.catalog.models import Scent


def tally_tags(selected_option_tag_lists):
    """selected_option_tag_lists: list of lists of tag strings (one list per answered question)."""
    counter = Counter()
    for tags in selected_option_tag_lists:
        counter.update(tags)
    return counter


def match_scent(tag_counter, current_season=None):
    """Returns the best-matching Scent for a given tag tally, or None if no scents exist."""
    scents = list(Scent.objects.prefetch_related("memory_tags"))
    if not scents:
        return None

    scored = []
    for scent in scents:
        scent_tags = {mt.tag for mt in scent.memory_tags.all()}
        overlap_score = sum(tag_counter.get(tag, 0) for tag in scent_tags)
        season_bonus = 1 if current_season and scent.season == current_season else 0
        scored.append((overlap_score, season_bonus, scent.name, scent))

    # Highest overlap first, then season match, then alphabetical for determinism
    scored.sort(key=lambda row: (-row[0], -row[1], row[2]))
    return scored[0][3]
