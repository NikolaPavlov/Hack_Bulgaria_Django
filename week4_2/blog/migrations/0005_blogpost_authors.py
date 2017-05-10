# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 06:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_auto_20170322_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='authors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
