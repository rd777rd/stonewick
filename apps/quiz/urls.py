from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.quiz_start, name="start"),
    path("take/", views.quiz_take, name="take"),
    path("result/<int:pk>/", views.quiz_result, name="result"),
]
