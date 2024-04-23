from django.urls import path

from .views import QuizCreateView, QuizDeleteView, QuizDetailView, QuizListView, QuizUpdateView


urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('new/', QuizCreateView.as_view(), name='quiz_new'),
    path('<slug:slug>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('<slug:slug>/edit/', QuizUpdateView.as_view(), name='quiz_edit'),
    path('<slug:slug>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
]
