from django.contrib import admin
from django.db import transaction

from .aiken import load

# from .extract import extract_questions
from .forms import QuizAdminForm
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
    search_fields = ('text',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_display = ('title', 'description', 'unit', 'year_tested', 'related_topic', 'paper_type')
    fields = ('title', 'description', 'unit', 'year_tested', 'related_topic', 'paper_type', 'file')
    search_fields = ('title',)

    def parse_quiz_file(self, file, quiz):
        content = file.read().decode('utf-8')
        aiken = load(content)
        print(aiken)

        if aiken is None:
            print("Failed to load questions from file")
            return

        # Create a new question for each parsed question
        for question_text, options, answer, feedback_text in aiken:
            try:
                question = Question.objects.create(text=question_text, quiz=quiz)
                print(f"Created question: {question}")

                # Create a new choice for each option
                for option_label, option_text in options:
                    is_correct = option_label == answer
                    choice = Choice.objects.create(text=option_text, is_correct=is_correct, question=question)
                    print(f"Created choice: {choice}")

                # Create a new feedback for each question
                feedback = Feedback.objects.create(text=feedback_text, question=question)
                print(f"Created feedback: {feedback}")
            except Exception as e:
                print(f"Failed to save question: {e}")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        file = form.cleaned_data.get('file')

        if file:
            with transaction.atomic():
                self.parse_quiz_file(file, obj)

    # def save_questions(self, questions, quiz):
    #     for question_data in questions:
    #         question = Question.objects.create(text=question_data['text'], quiz=quiz, related_topic=quiz.related_topic)

    #         for choice_text in question_data['choices']:
    #             is_correct = (choice_text == question_data['answer'])
    #             Choice.objects.create(text=choice_text, is_correct=is_correct, question=question)

    #         Feedback.objects.create(text=question_data['feedback'], question=question)

    # def parse_quiz_file(self, file, quiz):
    #     contents = file.read().decode('utf-8')
    #     print(contents)
    #     questions = extract_questions([contents])
    #     self.save_questions(questions, quiz)
