# api/urls.py
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, QuizViewSet


router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('mcq/', include(router.urls)),
]
