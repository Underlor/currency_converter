from __future__ import absolute_import, unicode_literals
import os

import django
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_converter.settings')

django.setup()

app = Celery('currency_converter')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from converter.tasks import parse_exchange_rates_task
    sender.add_periodic_task(crontab(hour=0, minute=0), parse_exchange_rates_task.s())
    # sender.add_periodic_task(crontab(minute='*/1'), parse_exchange_rates_task.s())
