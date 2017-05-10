from django.db import models


# Create your models here.
class User(models.Model):
    identifier = models.UUIDField(blank=True)

    def __str__(self):
        return str(self.identifier)


class Data(models.Model):
    key = models.TextField()
    value = models.TextField()
    user = models.ForeignKey(User)

    def __str__(self):
        return 'key:' + self.key + ' value:' + self.value + ' user:' + str(self.user)
