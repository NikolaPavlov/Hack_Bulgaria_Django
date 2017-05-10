from django.db import models
from django.utils import timezone


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, *kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    author_email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    post = models.ForeignKey('BlogPost')

    def __str__(self):
        return self.author_email
