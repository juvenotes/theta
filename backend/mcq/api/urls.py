# mcq/urls.py
from django.urls import path

from .views import QuestionDetailView, QuestionListView, QuizDetailView, QuizListView


urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('quizzes/<int:quiz_pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/<int:quiz_pk>/questions/', QuestionListView.as_view(), name='question_list'),
    path('quizzes/<int:quiz_pk>/questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
]
