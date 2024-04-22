from django.contrib import admin

from .models import Choice, Feedback, Question, Quiz, Unit


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline, FeedbackInline]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass
