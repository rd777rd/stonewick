from django.contrib import admin
from .models import QuizQuestion, QuizOption, ScentMemoryTag, QuizResult


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 2


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "order")
    inlines = [QuizOptionInline]


@admin.register(ScentMemoryTag)
class ScentMemoryTagAdmin(admin.ModelAdmin):
    list_display = ("scent", "tag")
    list_filter = ("tag",)


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("matched_scent", "user", "created_at")
    readonly_fields = ("answer_tags",)
