from django.db import models

class YearOfStudy(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return f"Year {self.year}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    year_of_study = models.ForeignKey(YearOfStudy, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class ShortAnswerQuestion(models.Model):
    title = models.CharField(max_length=255)
    year_created = models.IntegerField()
    question_text = models.TextField()
    answer_text = models.TextField()
    feedback_text = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title