import os
from celery import Celery

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsboard.settings')

app = Celery('newsboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()




app.conf.beat_schedule = {
    'send_email_every_monday_8am': {
        'task': 'SendEmail',
        'schedule': crontab(),
        #'args': (agrs),
    },
}