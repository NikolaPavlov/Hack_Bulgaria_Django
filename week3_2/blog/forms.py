from django.forms import ModelForm
from .models import BlogPost, Comment


class CreatePostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        # fields = ('title', 'content')


class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ('author_email', 'content')
