# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 05:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogpost_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]