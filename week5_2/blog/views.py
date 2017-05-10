from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from blog.models import BlogPost, Comment, Tag
from .forms import LoginForm, CommentForm, RegisterUserForm, BlogPostForm
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
        # if user is None:
        #     form.add_error(field='', error='No such user! Try again mf!')
    return render(request, 'blog/login.html', locals())


def register_view(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect(reverse(login_view))
        return redirect(reverse(register_view))

    return render(request, 'blog/register.html', locals())


def logout_view(request):
    logout(request)
    return redirect(reverse(index))


def index(request):
    '''
        loged in users see public + private posts
        not logged users see only public posts
    '''
    if request.user.is_authenticated():
        public_posts = list(BlogPost.objects.get_public_posts())
        private_posts = list(BlogPost.objects.get_private_posts())
        all_blog_posts = public_posts + private_posts
    else:
        all_blog_posts = BlogPost.objects.get_public_posts()

    return render(request, 'blog/index.html', locals())


@login_required(login_url=reverse_lazy('login_url'))
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
def create_blog_post(request):
    form = BlogPostForm()
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(index))

    return render(request, 'blog/create_post.html', locals())
