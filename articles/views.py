from django.shortcuts import render
from django.views.generic import (
	TemplateView,
	ListView,
	CreateView,
	DetailView,
	UpdateView,
	DeleteView,
	)
from .models import Article
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.


class ArticleListView(ListView):
	model = Article
	template_name = 'article_list.html'

class ArticleCreateView(LoginRequiredMixin, CreateView):
	model = Article
	template_name = 'article_new.html'
	fields = ('title', 'summary', 'photo', 'body')
	login_url = 'login'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class ArticleDetailView(DetailView):
	model = Article
	template_name = 'article_detail.html'

class ArticleUpdateView(UserPassesTestMixin, UpdateView):
	model = Article
	template_name = 'article_edit.html'
	fields = ('title', 'summary', 'body', 'photo')

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class ArticleDeleteView(UserPassesTestMixin, DeleteView):
	model = Article
	template_name = 'article_delete.html'
	success_url = reverse_lazy('article_list')

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user