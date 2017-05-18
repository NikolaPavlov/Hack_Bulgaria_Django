from pytube import YouTube


def video_is_available(youtube_link):
    try:
        yt = YouTube(youtube_link)
        return True
    except:
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
