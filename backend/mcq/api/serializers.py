# api/serializers.py
from rest_framework import serializers

from ..models import Choice, Feedback, Question, Quiz


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    feedbacks = FeedbackSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'quiz', 'slug', 'choices', 'feedbacks']
