from django import forms


class YouTubeUrlForm(forms.Form):
    link = forms.CharField(label='Youtube link', max_length=255)
    email = forms.EmailField()
