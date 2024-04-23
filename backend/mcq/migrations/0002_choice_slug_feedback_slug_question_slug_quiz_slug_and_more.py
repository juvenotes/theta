# Generated by Django 5.0.4 on 2024-04-22 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('question', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together={('question', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('quiz', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='quiz',
            unique_together={('unit', 'slug')},
        ),
        migrations.AlterUniqueTogether(
            name='unit',
            unique_together={('title', 'slug')},
        ),
    ]
