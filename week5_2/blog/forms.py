from django import forms
from .models import BlogPost


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    address = forms.CharField(max_length=250)
    apartment = forms.IntegerField()
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    post_code = forms.IntegerField()
    email = forms.EmailField()
    phone = forms.IntegerField()


class CommentForm(forms.Form):
    email = forms.EmailField(label='Your email')
    content = forms.CharField(label='Your comment:', widget=forms.Textarea)


class BlogPostForm(forms.ModelForm):
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tags'].required = False

    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'tags', 'is_private')
