import datetime

from django.db import models
from django.utils.text import slugify


# unit model
class Unit(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# quiz model
class Quiz(models.Model):
    YEAR_CHOICES = [(r,r) for r in range(2000, (datetime.datetime.now().year+1))]

    title = models.CharField(max_length=255)
    description = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    # New fields, for year and tags when we bundle quizzes and create a unified qbank for a unit if someone wants it
    year_tested = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    tags = models.CharField(max_length=255, default=unit)  # default is the unit this quiz belongs to, in future will be topic
    paper_type = models.CharField(max_length=255, choices=[('EOR', 'End of Rotation'), ('EOY', 'End of Year')], default='EOR')

    class Meta:
        unique_together = ('unit', 'slug')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.tags:
            self.tags = str(self.unit)  # convert unit to string
        super().save(*args, **kwargs)


# question model
class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    class Meta:
        unique_together = ('quiz', 'slug')

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        super().save(*args, **kwargs)

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

