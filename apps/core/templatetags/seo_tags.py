from django import template

register = template.Library()


@register.inclusion_tag("partials/_product_jsonld.html", takes_context=True)
def product_jsonld(context, product):
    return {"product": product, "request": context["request"]}


@register.inclusion_tag("partials/_faq_jsonld.html")
def faq_jsonld(faqs):
    """faqs: list of (question, answer) tuples"""
    return {"faqs": faqs}


@register.inclusion_tag("partials/_org_jsonld.html", takes_context=True)
def org_jsonld(context):
    return {"request": context["request"]}


@register.inclusion_tag("partials/_breadcrumb_jsonld.html", takes_context=True)
def breadcrumb_jsonld(context, crumbs):
    """crumbs: list of (name, url_or_None) tuples, in order from Home to current page.
    A None url marks the current page (no link needed for the last crumb)."""
    return {"crumbs": crumbs, "request": context["request"]}
