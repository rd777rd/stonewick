from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from apps.orders.models import Order
from apps.quiz.models import QuizResult
from apps.subscriptions.models import Subscription
from .forms import SignUpForm


class StonewickLoginView(LoginView):
    template_name = "accounts/login.html"


class StonewickLogoutView(LogoutView):
    pass


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)[:10]
    subscriptions = Subscription.objects.filter(user=request.user).select_related("product", "current_scent")
    quiz_results = QuizResult.objects.filter(user=request.user).select_related("matched_scent")[:5]
    return render(request, "accounts/dashboard.html", {
        "orders": orders,
        "subscriptions": subscriptions,
        "quiz_results": quiz_results,
    })
