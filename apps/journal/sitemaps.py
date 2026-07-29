from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at
