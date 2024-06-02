# api/serializers.py
from rest_framework import serializers

from ..models import Choice, Feedback, Question, Quiz


class QuizSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)
    class Meta:
        model = Quiz
        fields = ['id', 'unit', 'title', 'description', 'file', 'year', 'paper_type', 'related_topic']

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
        fields = ['id', 'text', 'quiz', 'choices', 'feedbacks']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        feedbacks_data = validated_data.pop('feedbacks')
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        for feedback_data in feedbacks_data:
            Feedback.objects.create(question=question, **feedback_data)
        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices')
        feedbacks_data = validated_data.pop('feedbacks')
        instance.text = validated_data.get('text', instance.text)
        instance.quiz = validated_data.get('quiz', instance.quiz)
        instance.save()

        for choice_data in choices_data:
            Choice.objects.update_or_create(question=instance, **choice_data)
        for feedback_data in feedbacks_data:
            Feedback.objects.update_or_create(question=instance, **feedback_data)

        return instance
