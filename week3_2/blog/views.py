from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import BlogPost, Tag
from .forms import CreatePostForm, CreateCommentForm


# Create your views here.
def index(request):
    all_blog_posts = BlogPost.objects.all()
    return render(request, 'index.html', locals())


def detail(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.method == 'GET':
        comments = post.comment_set.all()
        form = CreateCommentForm()
        return render(request, 'detail.html', locals())


def blog_post_create(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse(index))
    else:
        return render(request, 'create_post.html', locals())
