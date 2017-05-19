from datetime import *

from pytube import YouTube


def video_is_available(youtube_link):
    '''
    check if there is video behind the link
    '''
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


def time_until_midnight():
    '''
    calculate time left until midnight
    remove the microseconds from the calculated result
    retunrn 18:22:11[.xxx]  ---> [.xxx] part is removed
    '''
    tomorrow = date.today() + timedelta(1)
    midnight = datetime.combine(tomorrow, time())
    now = datetime.now()
    time_left_until_midnight = midnight - now
    time_withowth_microsec = str(time_left_until_midnight).split(".")[0]
    return time_withowth_microsec
