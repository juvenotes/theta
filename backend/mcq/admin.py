from django.contrib import admin
from django.db import transaction

from unfold.admin import ModelAdmin

from .aiken import load
from .forms import QuizAdminForm
from .models import Choice, Feedback, Question, Quiz, Unit


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 1

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    inlines = [ChoiceInline, FeedbackInline]
    search_fields = ('text',)

@admin.register(Unit)
class UnitAdmin(ModelAdmin):
    search_fields = ('name',)

@admin.register(Quiz)
class QuizAdmin(ModelAdmin):
    form = QuizAdminForm
    list_display = ('owner','title', 'description', 'unit', 'year', 'related_topic', 'paper_type')
    fields = ('owner','title', 'description', 'unit', 'year', 'related_topic', 'paper_type', 'file')
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        file = form.cleaned_data.get('file')

        if file:
            with transaction.atomic():
                content = file.read().decode('utf-8')
                aiken = load(content, obj)  # Pass the quiz object to the load function
                if aiken is None:
                    print("Failed to load questions from file")