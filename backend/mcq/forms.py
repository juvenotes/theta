from django import forms

from .models import Quiz


class QuizAdminForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Quiz
        fields = forms.ALL_FIELDS
