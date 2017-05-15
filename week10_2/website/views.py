from celery import chain
from django.shortcuts import redirect, render

from .forms import YouTubeUrlForm
from .tasks import download_video, mp4_to_mp3, send_email

# Create your views here.
def index(request):
    form = YouTubeUrlForm()
    if request.method == 'GET':
        return render(request, 'website/index.html', locals())

    if request.method == 'POST':
        form = YouTubeUrlForm(request.POST)
        if form.is_valid():
            youtube_link = form.cleaned_data['link']
            email = form.cleaned_data['email']
            dl_task = chain(download_video.s(youtube_link) | mp4_to_mp3.s() | send_email.s(email))
            dl_task.delay()
            return redirect(thanks)
        else:
            return render(request, 'website/index.html', locals())


def thanks(request):
    return render(request, 'website/thanks.html', {})
