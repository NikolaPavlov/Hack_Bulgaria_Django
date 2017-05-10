from __future__ import absolute_import, unicode_literals

import os
import glob

import sendgrid
import moviepy.editor as mp

from celery import shared_task
from pytube import YouTube
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.mail import EmailMessage

from week10_2 import settings
from sendgrid.helpers.mail import Email, Content, Mail, Attachment
import base64


@shared_task
def download_video(link):
    '''
    download the video and return it's filename
    '''
    yt = YouTube(link)
    video = yt.get('mp4', '720p')
    video.download(settings.MEDIA_ROOT)
    return yt.filename


def get_youtube_name(link):
    yt = YouTube(link)
    return yt.filename


@shared_task
def mp4_to_mp3(filename):
    '''
    1. Convert the mp3 into mp4
    2. Remove the mp3
    '''
    mp4_file_name = filename + '.mp4'
    mp4_file = os.path.join(settings.MEDIA_ROOT, mp4_file_name)
    if os.path.exists(mp4_file):
        f = mp.AudioFileClip(mp4_file)
        mp3_file_name = filename + '.mp3'
        mp3_file = os.path.join(settings.MEDIA_ROOT, mp3_file_name)
        f.write_audiofile(mp3_file)
        os.remove(mp4_file)


def send_mail(filename, email):
    # provider dosent serve big files :(
    # TODO fix
    file_mp3 = os.path.join(settings.MEDIA_ROOT, filename)
    mail = EmailMultiAlternatives(
        subject=filename,
        body='This is a simple email body',
        from_email='GRRRRR@gmail.com',
        to=[email],
        headers={"Reply-To": "GRRRRR@gmail"}
    )

    mail.template_id='53f806f5-7a75-4775-a11a-4e238f41023c'

    mail.attach_alternative(
        "<h1>This is mail.attach_alternative </<h1>", "text/html"
    )

    # with open(file_mp3, 'rb') as f:
    #     mail.attachments = [
    #         (file_mp3, f.read(), 'application/mp3')
    #     ]

    mail.send()



