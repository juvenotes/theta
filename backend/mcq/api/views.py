# mcq/views.py
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..aiken import load
from ..models import Question, Quiz
from .serializers import QuestionSerializer, QuizSerializer


class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def destroy(self, request, *args, **kwargs):
        quiz = self.get_object()
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionListView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_queryset(self):
        return Question.objects.filter(quiz_id=self.kwargs['quiz_pk'])

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)
        if file:
            questions = load(file)
            quiz = get_object_or_404(Quiz, pk=self.kwargs['quiz_pk'])
            for question_data in questions:
                question = Question(quiz=quiz, **question_data)
                question.save()
        return self.create(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer

    def get_object(self):
        return get_object_or_404(Question, quiz_id=self.kwargs['quiz_pk'], pk=self.kwargs['question_pk'])

    def destroy(self, request, *args, **kwargs):
        question = self.get_object()
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
