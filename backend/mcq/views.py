from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Quiz


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerQuizMixin(OwnerMixin):
    model = Quiz
    fields = ['title', 'description', 'unit', 'year_tested', 'related_topic', 'paper_type', 'file']
    success_url = reverse_lazy('quiz_list')

class OwnerQuizEditMixin(OwnerQuizMixin, OwnerEditMixin):
    template_name = 'mcq/dashboard/quiz/form.html'

class ManageQuizView(OwnerQuizMixin, ListView):
    template_name = 'mcq/dashboard/quiz/list.html'


class QuizCreateView(OwnerQuizEditMixin, CreateView):
    # model = Quiz
    # template_name = 'mcq/dashboard/quiz/new.html'
    # fields = ('title', 'description', 'unit', 'year_tested',
    #           'related_topic', 'paper_type', 'file')
    pass


# class QuizDetailView(DetailView):
#     model = Quiz
#     template_name = 'quiz_detail.html'

#     def get_object(self, queryset=None):
#         return get_object_or_404(Quiz, id=self.kwargs.get('id'))


class QuizUpdateView(OwnerQuizEditMixin, UpdateView):
    pass


class QuizDeleteView(OwnerQuizMixin, DeleteView):
    template_name = 'dashboard/quiz/delete.html'
