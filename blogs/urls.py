from django.urls import path
from .views import blog_detail, postComment, shareBlog, writeBlog

app_name = 'blog'

urlpatterns = [
    path('<int:id>/', blog_detail, name='detail'),
    path('comment/', postComment, name='comment'),
    path('blog/share/', shareBlog, name='share'),
    path('write/', writeBlog, name='write'),
]
