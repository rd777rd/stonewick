from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.catalog.models import Product
from apps.journal.models import Post
from apps.orders.models import Order
from .forms import ContactForm

FAQS = [
    (
        "Are the refill pouches recyclable or compostable?",
        "Our refill pouches are fully compostable at home or through municipal "
        "composting -- no separating layers or special drop-off required.",
    ),
    (
        "How long does one refill pouch last?",
        "Most refill pouches provide 40-60 hours of burn time or roughly 4-6 "
        "weeks of regular diffuser use, depending on the vessel size.",
    ),
    (
        "Can I change my subscription scent anytime?",
        "Yes -- from your account dashboard you can swap scents, skip a "
        "shipment, or pause your subscription at any time.",
    ),
]


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_vessels"] = Product.objects.filter(
            product_type=Product.ProductType.VESSEL, is_active=True
        ).select_related("category")[:4]
        ctx["featured_refills"] = Product.objects.filter(
            product_type=Product.ProductType.REFILL, is_active=True
        ).select_related("category", "scent")[:4]
        ctx["latest_posts"] = Post.objects.filter(is_published=True)[:3]

        # Vessel-first purchase path: first-time visitors see the
        # quiz/vessel story; customers who already own a vessel get sent
        # straight to reordering refills instead.
        ctx["is_returning_customer"] = (
            self.request.user.is_authenticated
            and Order.objects.filter(user=self.request.user, status=Order.Status.PAID).exists()
        )
        return ctx


class AboutView(TemplateView):
    template_name = "core/about.html"


class FAQView(TemplateView):
    template_name = "core/faq.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["faqs"] = FAQS
        return ctx


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out -- we'll reply within 1-2 business days.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


def robots_txt(request):
    disallow_paths = ["/cart/", "/accounts/dashboard/", "/admin/", "/subscriptions/manage/"]
    return render(request, "core/robots.txt", {"disallow_paths": disallow_paths}, content_type="text/plain")
