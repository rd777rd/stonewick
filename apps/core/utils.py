"""Small shared helpers used across apps (kept dependency-free and easily testable)."""
from datetime import date


def get_current_season(today: date = None) -> str:
    """
    Returns 'spring', 'summer', 'autumn', or 'winter' based on the current
    (Northern Hemisphere) calendar month. Used to: (1) apply the matching
    seasonal accent color site-wide via a <body> class, and (2) give the
    Scent Memory Quiz a tie-break bonus toward in-season scents.
    """
    today = today or date.today()
    month = today.month
    if month in (3, 4, 5):
        return "spring"
    if month in (6, 7, 8):
        return "summer"
    if month in (9, 10, 11):
        return "autumn"
    return "winter"
