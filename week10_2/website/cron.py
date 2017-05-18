import kronos
import random

from website.models import Statistics


@kronos.register('0 0 * * *')
def reset_statistic():
    Statistics.objects.all().delete()
