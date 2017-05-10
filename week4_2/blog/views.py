from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from blog.models import BlogPost, Tag, Comment
from .forms import LoginForm, CreatePostForm, CommentForm
from django.utils import timezone


# Create your views here.
def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
        if user is not None:
            login(request, user)
            return redirect(reverse(index))
        if user is None:
            form.add_error(field='', error='No such user! Try again mf!')
    return render(request, 'blog/login.html', locals())


def logout_view(request):
    logout(request)
    return redirect(reverse(index))


def profile_view(request):
    return render(request, 'blog/profile.html', locals())


def index(request):
    all_blog_posts = BlogPost.objects.all()
    return render(request, 'blog/index.html', locals())


def detail_post_view(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    tags = post.tags.all()
    comments = post.comment_set.all().order_by('created_at')

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            Comment.objects.create(
                author_email=form.cleaned_data['email'],
                content=form.cleaned_data['content'],
                created_at=timezone.now(),
                post=post)

            return redirect(reverse(detail_post_view, args=[post_id]))
        else:
            form.add_error(field='', error='Invalid form dude, try again')

    return render(request, 'blog/detail.html', locals())


@login_required(login_url=reverse_lazy('login_url'))
def create_post(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse(index))

    return render(request, 'blog/create_post.html', locals())
