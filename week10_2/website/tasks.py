from __future__ import absolute_import, unicode_literals

import os
import uuid

import sendgrid
import moviepy.editor as mp

from celery import shared_task
from pytube import YouTube
from django.core.mail import EmailMessage, EmailMultiAlternatives
from sendgrid.helpers.mail import Content, Email, Mail

from week10_2 import settings


@shared_task
def download_video(youtube_link):
    '''
    FIRST CELERY TASK
    download the video and return it's filename + uuid4
    '''
    yt = YouTube(youtube_link)
    video = yt.get_videos()[-1] # -1 will select the best possible format
    video.download(settings.MEDIA_ROOT)
    return yt.filename + '***' + str(uuid.uuid4())


@shared_task
def mp4_to_mp3(filename):
    '''
    SECOND CELERY TASK
    strip spaces from the filename and remove uuid4 part
    convert it from mp4 to mp3
    remove the mp4 and return filename.mp3 string
    '''
    filename = filename.split('***')[0]
    # mp4_file_name = filename + '.mp4'
    mp4_file_name = filename + '.webm'
    mp4_file = os.path.join(settings.MEDIA_ROOT, mp4_file_name)
    if os.path.exists(mp4_file):
        f = mp.AudioFileClip(mp4_file)
        filename = str(filename).replace(' ', '_')
        mp3_file_name = filename + '.mp3'
        mp3_file = os.path.join(settings.MEDIA_ROOT, mp3_file_name)
        f.write_audiofile(mp3_file)
        os.remove(mp4_file)
    return str(mp3_file_name)


@shared_task
def send_email(filename, email):
    '''
    THIRD CELERY TASK
    '''
    link = "<a href='http://localhost:8000{}'>{}</a>".format(
        settings.MEDIA_URL + filename, filename)

    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    from_email = Email('youtube_convertor@gmail')
    subject = filename
    to_email = Email(email)
    content = Content('text/html', link)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
