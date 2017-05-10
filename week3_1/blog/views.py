from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import BlogPost, Comment, Tag


# Create your views here.
def index(request):
    all_blog_posts = BlogPost.objects.all()
    return render(request, 'index.html', locals())


def detail(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    if request.method == 'POST':
        comment = request.POST['comment']
        author_email = request.POST['author_email']
        Comment.objects.create(author_email=author_email,
                               content=comment,
                               post=post)
        # redirect to the same page (auto refresh)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.method == 'GET':
        comments = post.comment_set.all()
        tags = post.tag_set.all()
        return render(request, 'detail.html', locals())


def blog_post_create(request):
    if request.method == "GET":
        return render(request, 'create_post.html', {})

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        blog_post = BlogPost(title=title, content=content)
        blog_post.save()

        tags = request.POST['tags']
        tags_splited = tags.split(',')
        for t in tags_splited:
            tag = Tag(name=t)
            tag.save()
            tag.posts.add(blog_post)
        return HttpResponseRedirect('/')
