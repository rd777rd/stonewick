from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from apps.catalog.sitemaps import ProductSitemap, CategorySitemap
from apps.journal.sitemaps import PostSitemap
from apps.core.sitemaps import StaticViewSitemap
from apps.core.views import robots_txt

sitemaps = {
    "products": ProductSitemap,
    "categories": CategorySitemap,
    "posts": PostSitemap,
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls", namespace="core")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("shop/", include("apps.catalog.urls", namespace="catalog")),
    path("quiz/", include("apps.quiz.urls", namespace="quiz")),
    path("subscriptions/", include("apps.subscriptions.urls", namespace="subscriptions")),
    path("cart/", include("apps.orders.urls", namespace="orders")),
    path("journal/", include("apps.journal.urls", namespace="journal")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
