from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .query import BlogPostQuerySet


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts')
    authors = models.ManyToManyField(User)
    is_private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    objects = BlogPostQuerySet.as_manager()


class Tag(models.Model):
    tag_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag_name


class Comment(models.Model):
    author_email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('BlogPost')

    def __str__(self):
        return 'AuthorEmail: ' + self.author_email
