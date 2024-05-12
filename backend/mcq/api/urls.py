# mcq/urls.py
from django.urls import path

from .views import (
    QuestionDetailView,
    QuestionListView,
    QuizCreateView,
    QuizDetailView,
    QuizListView,
)


urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),  # GET to list quizzes
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz_create'),  # POST here to create a quiz
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),  # GET, PUT, PATCH, DELETE for a specific quiz
    path('quizzes/<int:quiz_pk>/questions/', QuestionListView.as_view(), name='question_list'),  # GET to list questions of a quiz, POST here to add questions to a quiz
    path('quizzes/<int:quiz_pk>/questions/<int:question_pk>/', QuestionDetailView.as_view(), name='question_detail'),  # GET, PUT, PATCH, DELETE for a specific question
]
