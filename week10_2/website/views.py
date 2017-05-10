from celery import chain

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render

from .forms import YouTubeUrlForm
from .tasks import download_video, mp4_to_mp3, get_youtube_name


# Create your views here.
def index(request):
    form = YouTubeUrlForm()
    if request.method == 'GET':
        return render(request, 'website/index.html', locals())

    if request.method == 'POST':
        '''
        checks to be done:
            1. Is the link valid?
            2. Is the duration in MAX_DURATION
            3. Is daily limit reach
        '''
        form = YouTubeUrlForm(request.POST)
        if form.is_valid():
            youtube_link = form.cleaned_data['link']
            email = form.cleaned_data['email']
            '''
            celery chain:
                1. download the video
                2. convert the dl video to mp3
                3. send the mail with link to the MEDIA file
            '''
            # switch to chort? ( dl | convert | email send )
            dl_task = chain(download_video.s(youtube_link) | mp4_to_mp3.s())
            dl_task.delay()
            return redirect(thanks)
        else:
            return render(request, 'website/index.html', locals())


def thanks(request):
    return render(request, 'website/thanks.html', {})
