import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')

app = Celery('newsportal', broker='redis://127.0.0.1:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_every_mon_8am': {
        'task': 'news.tasks.send_last_week_posts',
        'schedule': crontab(minute='*/2')
    }
}
