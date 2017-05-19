from celery import chain
from django.shortcuts import redirect, render, reverse

from .forms import YouTubeUrlForm
from .tasks import download_video, mp4_to_mp3, send_email
from .utils.helpers import get_client_ip, video_is_available, time_until_midnight

from week10_2 import settings
from website.models import Statistics


def index(request):
    form = YouTubeUrlForm()
    ip = get_client_ip(request)
    stats, created = Statistics.objects.get_or_create(ip=ip)
    daily_downloads = stats.daily_downloads
    time_left_until_next_dl = time_until_midnight()
    if request.method == 'POST':
        form = YouTubeUrlForm(request.POST)
        if form.is_valid():
            youtube_link = form.cleaned_data['link']
            email = form.cleaned_data['email']
            if video_is_available(youtube_link):
                if stats.daily_downloads <= settings.DAILY_LIMIT:
                    dl_task = chain(download_video.s(youtube_link) |
                                    mp4_to_mp3.s() |
                                    send_email.s(email))
                    dl_task.delay()
                    stats.daily_downloads += 1
                    stats.save()
                    success_msg = 'Email with the link to the file is on the way to your email'
                    form = YouTubeUrlForm()
                else:
                    form_errors_limit = 'Daily limit reached!'
            else:
                form_errors_broken_link = 'Check the link for errors, can\'t find the video!'
    return render(request, 'website/index.html', locals())


def thanks(request):
    return render(request, 'website/thanks.html', {})
