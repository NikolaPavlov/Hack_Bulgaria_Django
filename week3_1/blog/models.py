from django.db import models
from django.utils import timezone


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=254, unique=True)
    # created_at = models.DateTimeField(timezone.now)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=254)
    posts = models.ManyToManyField('BlogPost')

    def __str__(self):
        return self.name


class Comment(models.Model):
    author_email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    post = models.ForeignKey('BlogPost')

    def __str__(self):
        return self.author_email
