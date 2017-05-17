from celery import chain
from django.shortcuts import redirect, render

from .forms import YouTubeUrlForm
from .tasks import download_video, mp4_to_mp3, send_email

from week10_2 import settings
from website.models import Statistics

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    form = YouTubeUrlForm()
    ip = get_client_ip(request)
    stats, created = Statistics.objects.get_or_create(ip=ip)
    daily_downloads = stats.daily_downloads
    return render(request, 'website/index.html', locals())

    if request.method == 'POST':
        form = YouTubeUrlForm(request.POST)

        if form.is_valid():
            if stats.daily_downloads <= settings.DAILY_LIMIT:
                youtube_link = form.cleaned_data['link']
                email = form.cleaned_data['email']
                dl_task = chain(download_video.s(youtube_link) |
                                mp4_to_mp3.s() |
                                send_email.s(email))
                dl_task.delay()
                stats.daily_downloads += 1
                stats.save()
                return redirect(thanks)
            else:
                return render(request, 'website/daily_limit.html', locals())

        else:
            return render(request, 'website/index.html', locals())


def thanks(request):
    return render(request, 'website/thanks.html', {})
