import uuid
from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now)


class Data(models.Model):
    key = models.TextField()
    value = models.TextField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now)
