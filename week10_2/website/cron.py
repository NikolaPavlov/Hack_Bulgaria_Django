from datetime import datetime
from .models import Statistics


def delete_yesterday_statistic():
    Statistics.objects.filter(created_at__lt=datetime.now()).delete()

def run():
    delete_yesterday_statistic()
