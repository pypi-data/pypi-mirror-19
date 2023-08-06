# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic import ListView, DetailView

from .models import Post


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(published=True)


class PostDetail(DetailView):
    model = Post
