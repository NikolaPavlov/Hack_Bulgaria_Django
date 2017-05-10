from django import forms
from .models import Offer, Category
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)


class AddOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('author', )
