# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 14:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_statistics_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistics',
            old_name='created_at',
            new_name='time_of_last_dl',
        ),
    ]
