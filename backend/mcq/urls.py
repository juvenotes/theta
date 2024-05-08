from django.urls import path

from .views import ManageQuizView, QuizCreateView, QuizDeleteView, QuizUpdateView


urlpatterns = [
    path('mine/', ManageQuizView.as_view(), name='quiz_list'),
    path('new/', QuizCreateView.as_view(), name='quiz_new'),
    path('<int:pk>/edit/', QuizUpdateView.as_view(), name='quiz_edit'),
    path('<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
]
