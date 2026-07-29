from django.urls import path
from . import views

app_name = "subscriptions"

urlpatterns = [
    path("manage/", views.manage, name="manage"),
    path("<int:pk>/pause/", views.pause, name="pause"),
    path("<int:pk>/resume/", views.resume, name="resume"),
    path("<int:pk>/skip/", views.skip, name="skip"),
    path("<int:pk>/swap-scent/", views.swap_scent, name="swap_scent"),
    path("<int:pk>/cancel/", views.cancel, name="cancel"),
]
