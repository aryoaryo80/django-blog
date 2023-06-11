from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.views.generic import UpdateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.models import User
from posts.models import Post
from django.core.paginator import Paginator
from django.db.models import Q


class HomeView(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        if search:
            posts = Post.objects.filter(
                Q(content__contains=search) | Q(title__contains=search))
            # search.num_page = search
        else:
            posts = Post.objects.all()
        can_search = True
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/home.html', {'posts': page_obj, 'can_search': can_search, 'search': search})
