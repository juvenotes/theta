from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Quiz


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz_list.html'

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz_detail.html'

class QuizCreateView(CreateView):
    model = Quiz
    template_name = 'quiz_new.html'
    fields = ('title', 'description', 'unit')

class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = 'quiz_edit.html'
    fields = ('title', 'description', 'unit')

class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'quiz_delete.html'
    success_url = reverse_lazy('quiz_list')
