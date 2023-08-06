# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from django_markdown.admin import MarkdownModelAdmin

from .models import Post


@admin.register(Post)
class PostAdmin(MarkdownModelAdmin):
    pass

