from .models import BlogModel, BlogComment
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_mail_task
from django.conf import settings
from .forms import BlogForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def writeBlog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('home')
        else:
            print('Blog Not Created')
    else:
        form = BlogForm()

    return render(request, 'blogs/create.html', context={'form': form})


def index(request):
    blogs = BlogModel.objects.all().select_related('author')
    if request.user.is_authenticated:
        request_user_blogs = BlogModel.objects.filter(author=request.user)
    else:
        request_user_blogs = 'Please Login to see your blogs'
    context = {
        'blogs': blogs,
        'rblogs': request_user_blogs,

    }
    return render(request, 'home.html', context=context)


def blog_detail(request, id):
    blog_obj = BlogModel.objects.get(id=id)
    comments = BlogComment.objects.filter(
        blog=blog_obj).select_related('cauthor')
    if request.user.is_authenticated:
        request_user_blogs = BlogModel.objects.filter(author=request.user)
    else:
        request_user_blogs = 'Please Login to see your blogs'

    context = {
        'blog': blog_obj,
        'rblogs': request_user_blogs,
        'comments': comments

    }
    return render(request, 'blogs/detail.html', context=context)


@csrf_exempt
def postComment(request):
    if request.method == 'POST':
        blog_id = request.POST.get('id')
        comment = request.POST.get('comment')
        blog_obj = BlogModel.objects.get(id=blog_id)
        if blog_obj:
            BlogComment.objects.create(
                comment=comment, cauthor=request.user, blog=blog_obj)

        subject = 'New Comment'
        blog_url = request.build_absolute_uri(blog_obj.get_absolute_url())

        message = f"{request.user.username} has posted a comment on your Blog {blog_url}"
        email_from = settings.EMAIL_HOST_USER
        recepient_list = [blog_obj.author.email]
        send_mail_task(subject=subject, message=message,
                       email_from=email_from, recepient_list=recepient_list)

        data = {
            'comment': comment,
            'author': request.user.username,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Error on posting comment"})


@csrf_exempt
def shareBlog(request):
    if request.method == 'POST':
        email = request.POST.get('user_email')
        id = request.POST.get('id')
        blog_obj = BlogModel.objects.get(id=id)

        subject = f'{request.user.username} shared a blog'
        url = request.build_absolute_uri(blog_obj.get_absolute_url())
        message = f'{request.user.username} has shared a blog with you, read it here {url}'
        email_from = settings.EMAIL_HOST_USER
        recepient_list = [email]
        send_mail_task(subject=subject, message=message,
                       email_from=email_from, recepient_list=recepient_list)
        return JsonResponse({'Success': 'Blog Shared Successfully'})
    else:
        return JsonResponse({'error': 'Could Not Share Blog'})
