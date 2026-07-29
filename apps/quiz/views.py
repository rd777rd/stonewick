from django.shortcuts import render, redirect
from django.urls import reverse

from apps.core.utils import get_current_season
from .forms import QuizAnswerForm
from .models import QuizQuestion, QuizOption, QuizResult
from .scoring import tally_tags, match_scent


def quiz_start(request):
    questions = QuizQuestion.objects.prefetch_related("options")
    return render(request, "quiz/start.html", {"questions": questions})


def quiz_take(request):
    if request.method == "POST":
        form = QuizAnswerForm(request.POST)
        if form.is_valid():
            selected_tag_lists = []
            for field_name, option_id in form.cleaned_data.items():
                option = QuizOption.objects.get(pk=option_id)
                selected_tag_lists.append(option.tag_list())

            tag_counter = tally_tags(selected_tag_lists)
            matched_scent = match_scent(tag_counter, current_season=get_current_season())

            if not request.session.session_key:
                request.session.create()

            result = QuizResult.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                matched_scent=matched_scent,
                answer_tags=list(tag_counter.elements()),
            )
            return redirect(reverse("quiz:result", args=[result.pk]))
    else:
        form = QuizAnswerForm()
    return render(request, "quiz/take.html", {"form": form})


def quiz_result(request, pk):
    result = QuizResult.objects.select_related("matched_scent").get(pk=pk)
    related_products = []
    if result.matched_scent:
        related_products = result.matched_scent.products.filter(is_active=True)
    return render(request, "quiz/result.html", {
        "result": result,
        "related_products": related_products,
    })
