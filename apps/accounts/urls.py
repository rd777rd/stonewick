from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.StonewickLoginView.as_view(), name="login"),
    path("logout/", views.StonewickLogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
