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
    prepopulated_fields = {'slug': ('text',)}
    search_fields = ('text',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ('name',)
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'unit', 'year_tested', 'tags', 'paper_type', 'slug')  # include 'slug' here
    fields = ('title', 'description', 'unit', 'year_tested', 'tags', 'paper_type', 'slug')  # include 'slug' here
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
