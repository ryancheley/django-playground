from django.contrib import admin

from core.admin import BaseModelAdmin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(BaseModelAdmin):
    pass
