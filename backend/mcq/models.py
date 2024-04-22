from django.db import models


# unit model
class Unit(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

# quiz model
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# question model
class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# choices model
class Choice(models.Model):
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# feedback model
class Feedback(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


