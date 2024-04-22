from django.urls import path

from .views import QuizCreateView, QuizDeleteView, QuizDetailView, QuizListView, QuizUpdateView


urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('new/', QuizCreateView.as_view(), name='quiz_new'),
    path('<int:pk>/edit/', QuizUpdateView.as_view(), name='quiz_edit'),
    path('<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
]
