from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from users.permissions import IsManagerOrContributor, IsManager

from ..aiken import load
from ..models import Question, Quiz
from .serializers import QuestionSerializer, QuizSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    permission_classes = [IsManagerOrContributor]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        # Only a Manager can remove a Contributor status, hence check for IsManager permission
        permission = IsManager()
        if not permission.has_permission(request, self):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_contributor:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_queryset(self):
        return Question.objects.filter(quiz_id=self.kwargs['quiz_pk'])

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)
        if file:
            questions = load(file)
            quiz = get_object_or_404(Quiz, pk=self.kwargs['quiz_pk'])
            for question_data in questions:
                question = Question(quiz=quiz, **question_data)
                question.save()
            return Response({'message': 'Questions created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)