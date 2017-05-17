from django.db import models

# Create your models here.
class Statistics(models.Model):
    ip = models.GenericIPAddressField()
    daily_downloads = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'ip: {}, daily_downloads: {}'.format(ip, daily_downloads)
