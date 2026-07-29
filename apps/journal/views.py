from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    posts = Post.objects.filter(is_published=True)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "journal/post_list.html", {"page_obj": page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "journal/post_detail.html", {"post": post})
