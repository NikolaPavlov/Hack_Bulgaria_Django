from django import forms
from .models import BlogPost, Comment


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'tags')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': 'Comment'
        }
