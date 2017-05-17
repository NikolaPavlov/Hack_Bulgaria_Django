#!/bin/bash

# https://bradmontgomery.net/blog/scheduled-tasks-or-cron-jobs-with-django/

# This is a Django, Project-specific Cron script.
# Separate Projects would need a copy of this script
# with appropriate Settings export statments.

PYTHONPATH="${PYTHONPATH}:/path/to/django/project/directory"
export PYTHONPATH
export DJANGO_SETTINGS_MODULE=mysite.settings

python/path/to/django/project/directory/mysite/cron.py
