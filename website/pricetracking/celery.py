from __future__ import absolute_import, unicode_literals

import os
from celery.schedules import crontab
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricetracking.settings')

app = Celery('pricetracking')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_for_updates': {
        'task': 'product.tasks.track_for_discount',
        'schedule': crontab(minute=0, hour='*/3'), 
    },
}