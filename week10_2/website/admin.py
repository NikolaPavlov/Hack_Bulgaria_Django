from django.contrib import admin
from .models import Statistics

# Register your models here.
@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('ip', 'daily_downloads', 'time_of_last_dl')

