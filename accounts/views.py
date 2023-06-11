from typing import Any
from django import http
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User
from .forms import *
from .mixin import NoLoginRequiredMixin
from posts.models import Post


class UserLoginView(NoLoginRequiredMixin, View):
    form_class = UserCreationForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'welcome to your account')
                return redirect('home:home')
            messages.error(
                request, 'your username/email or password is wrong!', 'warning')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:home')


class UserRegisterView(NoLoginRequiredMixin, View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd['username'], password=cd['password1'])
            user = authenticate(
                request, username=cd['username'], password=cd['password1'])
            login(request, user)
            messages.success(request, 'Register Successfully')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        posts = Post.objects.filter(user=request.user)
        return render(request, self.template_name, {'form': form, 'posts': posts})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile has been updated')
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})
