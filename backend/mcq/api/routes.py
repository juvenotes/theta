from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, QuizViewSet


router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'quizzes/<int:quiz_pk>/questions', QuestionViewSet, basename='question')

urlpatterns = router.urls