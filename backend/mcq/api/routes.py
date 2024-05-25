from .views import QuestionViewSet, QuizViewSet


routes = [
    {"regex": r"quizzes", "viewset": QuizViewSet, "basename": "quiz"},
    {"regex": r"quizzes/<int:quiz_pk>/questions", "viewset": QuestionViewSet, "basename": "question"},
]