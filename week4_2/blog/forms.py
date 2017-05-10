from django import forms
from .models import BlogPost, Comment
from django.utils import timezone


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'tags')


class CommentForm(forms.Form):
    email = forms.EmailField(label='Your email')
    content = forms.CharField(label='Your comment:', widget=forms.Textarea)


# class CommentForm(forms.ModelForm):
#
#     class Meta:
#         model = Comment
#         fields = ('author_email', 'content')
#         labels = {
#             'content': 'Comment'
#         }
