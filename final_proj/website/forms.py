from django import forms


class YouTubeUrlForm(forms.Form):
    link = forms.CharField(label='Youtube link', max_length=255, required=True)
    email = forms.EmailField(label='Your email', required=True)
