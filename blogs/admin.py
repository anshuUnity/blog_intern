from django.contrib import admin
from .models import BlogModel, BlogComment
# Register your models here.


@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish')
    search_fields = ('title',)


@admin.register(BlogComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'publish')
    search_fields = ('comment',)
