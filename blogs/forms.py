from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from .models import BlogComment, BlogModel


class BlogForm(ModelForm):
    class Meta:
        model = BlogModel
        fields = ('title', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
