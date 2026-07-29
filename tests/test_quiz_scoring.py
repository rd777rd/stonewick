import pytest

from apps.catalog.models import Scent
from apps.quiz.models import ScentMemoryTag
from apps.quiz.scoring import tally_tags, match_scent


@pytest.fixture
def scents(db):
    coastal = Scent.objects.create(
        name="Beach House Morning", memory_story="Salt air and screen doors.", season=Scent.Season.SUMMER
    )
    kitchen = Scent.objects.create(
        name="Grandma's Kitchen", memory_story="Cinnamon rolls on a Sunday.", season=Scent.Season.WINTER
    )
    ScentMemoryTag.objects.create(scent=coastal, tag="coastal")
    ScentMemoryTag.objects.create(scent=coastal, tag="summer")
    ScentMemoryTag.objects.create(scent=kitchen, tag="family-kitchen")
    ScentMemoryTag.objects.create(scent=kitchen, tag="cozy-winter")
    return coastal, kitchen


def test_tally_tags_combines_multiple_answers():
    result = tally_tags([["coastal", "summer"], ["coastal"]])
    assert result["coastal"] == 2
    assert result["summer"] == 1


def test_match_scent_picks_highest_overlap(scents):
    coastal, kitchen = scents
    tag_counter = tally_tags([["coastal", "summer"], ["coastal"]])
    result = match_scent(tag_counter)
    assert result == coastal


def test_match_scent_returns_none_when_no_scents_exist(db):
    tag_counter = tally_tags([["coastal"]])
    assert match_scent(tag_counter) is None


def test_match_scent_breaks_ties_with_season(scents):
    coastal, kitchen = scents
    # Equal overlap (1 tag each) but kitchen matches "current season"
    tag_counter = tally_tags([["summer"], ["cozy-winter"]])
    result = match_scent(tag_counter, current_season=Scent.Season.WINTER)
    assert result == kitchen
