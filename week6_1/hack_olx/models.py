from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='img/')
    category = models.ForeignKey(Category)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title
