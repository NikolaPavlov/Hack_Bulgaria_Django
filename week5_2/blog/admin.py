from django.contrib import admin
from .models import BlogPost, Tag, Comment


# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Comment)
