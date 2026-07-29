from django import forms
from .models import QuizQuestion


class QuizAnswerForm(forms.Form):
    """Dynamically built form: one ChoiceField per QuizQuestion."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in QuizQuestion.objects.prefetch_related("options"):
            field_name = f"question_{question.pk}"
            choices = [(opt.pk, opt.text) for opt in question.options.all()]
            self.fields[field_name] = forms.ChoiceField(
                choices=choices,
                label=question.text,
                widget=forms.RadioSelect,
                required=True,
            )
