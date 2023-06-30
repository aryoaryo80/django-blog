from typing import Any
from django import http
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.views.generic import UpdateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.contrib import messages
from accounts.models import User
from .forms import *
from .models import Post, Vote, Comment


class UserProfileView(View):

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.user == request.user:
            messages.success(request, 'Redirected to Your Profile')
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'posts/profile.html', {'user_instance': self.user})


class PostDetailView(View):
    form_class = CommentForm
    template_name = 'posts/detail.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'post': self.post_instance,
                       'comments': self.post_instance.comments.filter(is_sub=False),
                       'nform': NestedCommentForm,
                       'form': self.form_class})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        nform = NestedCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = self.post_instance
            form.save()
            messages.success(request, 'your comment has been created')
            return redirect('posts:detail', self.post_instance.slug)
        if nform.is_valid():
            Comment(
                content=nform.cleaned_data['body'],
                user=request.user,
                post=self.post_instance,
                is_sub=True,
                sub=get_object_or_404(
                    Comment, id=nform.cleaned_data['comment_id'])
            ).save()
            messages.success(request, 'your comment has been created')
            return redirect('posts:detail', self.post_instance.slug)
        return render(request, self.template_name,
                      {'post': self.post_instance, 'comments': self.post_instance.comments.all(), 'form': self.form_class})


class VoteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('post_id'):
            post = get_object_or_404(Post, id=kwargs['post_id'])
            instance = post.votes.filter(user=request.user)
            if instance.exists():
                messages.warning(
                    request, 'your like deleted', 'success')
                instance.delete()
                return redirect('posts:detail', post.slug)
            Vote.objects.create(
                user=request.user,
                content_object=post
            )
            messages.success(request, 'you liked this post', 'success')
            return redirect('posts:detail', post.slug)
        elif kwargs.get('comment_id'):
            comment = get_object_or_404(Comment, id=kwargs['comment_id'])
            instance = comment.votes.filter(user=request.user)
            if instance.exists():
                messages.warning(
                    request, 'your like deleted', 'warning')
                instance.delete()
                return redirect('posts:detail', comment.post.slug)
            Vote.objects.create(
                user=request.user,
                content_object=comment
            )
            return redirect('posts:detail', comment.post.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if post.user.id == request.user.id:
            post.delete()
        messages.success(request, 'your post has been deleted')
        return redirect('posts:profile', request.user.id)


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'posts/update.html'

    def setup(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class(instance=self.instance)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.instance)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(form.cleaned_data['title'][:100])
            post.save()
            messages.success(request, 'your post updated successfully')
            return redirect('posts:detail', post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'posts/create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.slug = slugify(form.cleaned_data['title'][:100])
            post.save()
            messages.success(request, 'your post created')
            return redirect('posts:detail', post.slug)
        return render(request, self.template_name, {'form': form})
