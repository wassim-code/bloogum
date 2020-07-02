from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
		ListView,
		CreateView,
		FormView,
		TemplateView,
		UpdateView,
		DeleteView,
		View,
	)

from .models import Post, Comment, Email
from .forms import *

class PostListView(ListView):
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.GET.get('search') is not None:
			context['search'] = self.request.GET.get('search')
		return context

	def get_queryset(self):
		try:
			queryset = Post.objects.filter(title__icontains=self.request.GET.get('search'))
			if queryset is None:
				queryset = Post.objects.filter(content__icontains=self.request.GET.get('search'))
			self.template_name = 'blog/search.html'
			return queryset.order_by('-pub_date')
		except:
			return Post.objects.all().order_by('-pub_date')

class UserPostsListView(ListView):
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['posts_count'] = self.get_queryset().count()
		context['author'] = self.kwargs['username']
		return context

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs['username'])
		queryset = Post.objects.filter(author=user).order_by('-pub_date')
		return queryset

class PostCommentsListView(ListView):
	context_object_name = 'comments'
	template_name = 'blog/post_comments.html'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
		context['comments_count'] = self.get_queryset().count()
		return context

	def get_queryset(self):
		post = get_object_or_404(Post, pk=self.kwargs['pk'])
		queryset = Comment.objects.filter(post=post).order_by('-pub_date')
		return queryset

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']
	template_name = 'blog/post_create_form.html'
	success_url = '/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, 'Post added successfully.')
		return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	fields = ['content']
	template_name = 'blog/comment_create_form.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post'] = get_object_or_404(Post, pk=self.kwargs['pk']).title
		return context

	def form_valid(self, form):
		form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
		form.instance.author =  self.request.user
		messages.success(self.request, 'Comment added successfully.')
		return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Comment
	fields = ['content']
	template_name = 'blog/comment_update_form.html'
	context_object_name = 'comment'

	def get_object(self):
		obj = get_object_or_404(Comment, pk=self.kwargs['pk'], post__pk=self.kwargs['post_pk'])
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['trun'] = self.get_object().content[:20] + '...'
		return context

	def form_valid(self, form):
		form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
		form.instance.author =  self.request.user
		messages.success(self.request, 'Comment updated successfully.')
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('post_detail', kwargs={'pk': self.get_object().post.pk})

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	context_object_name = 'comment'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['trun'] = self.get_object().content[:20] + '...'
		return context

	def get_object(self):
		obj = get_object_or_404(Comment, pk=self.kwargs['pk'], post__pk=self.kwargs['post_pk'])
		return obj

	def get_success_url(self):
		return reverse('post_detail', kwargs={'pk': self.get_object().post.pk})

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	template_name = 'blog/post_update_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, 'Post updated successfully.')
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	context_object_name = 'post'
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user

class ContactUsView(LoginRequiredMixin, CreateView):
	model = Email
	fields = ['subject', 'message']
	template_name = 'blog/contactus.html'
	success_url = '/'

	def form_valid(self, form):
		form.instance.sender = self.request.user
		messages.success(self.request, 'Your Email has been sent successfully!')
		return super().form_valid(form)

class SignUpView(FormView):
	form_class = SignUpForm
	template_name = 'registration/signup.html'
	success_url = '/login/'

	def form_valid(self, form):
		messages.success(self.request,
		 'Your account has been created successfully! You are now able to connect with your new account.')
		form.save()
		return super().form_valid(form)

class ProfileView(LoginRequiredMixin, View):
	def get(self, request):
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form': p_form})

	def post(self, request):
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Your account has been updated successfully!')
			return redirect('home')
		return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form': p_form})