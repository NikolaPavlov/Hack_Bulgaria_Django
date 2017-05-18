from django.db import models

# Create your models here.
class Statistics(models.Model):
    ip = models.GenericIPAddressField()
    daily_downloads = models.IntegerField(default=0)
    time_of_last_dl = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'ip: ' + self.ip
