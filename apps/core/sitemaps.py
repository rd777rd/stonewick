from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4

    def items(self):
        return ["core:home", "core:about", "core:faq", "core:contact", "quiz:start"]

    def location(self, item):
        return reverse(item)
