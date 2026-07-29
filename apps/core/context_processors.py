from django.conf import settings

from .utils import get_current_season


def site_meta(request):
    """
    Makes site-wide SEO/branding values available to every template without
    each view having to pass them explicitly. Individual templates can still
    override title/description via the {% block meta_title %} /
    {% block meta_description %} blocks in base.html.
    """
    protocol = getattr(settings, "SITE_PROTOCOL", "http")
    domain = getattr(settings, "SITE_DOMAIN", request.get_host())
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Stonewick"),
        "SITE_URL": f"{protocol}://{domain}",
        # Drives the seasonal accent color swap (see body class in base.html)
        # and the Scent Memory Quiz's in-season tie-break bonus -- updates
        # automatically with the calendar, no template or code edit needed.
        "current_season": get_current_season(),
    }
