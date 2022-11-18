# Note: for starting Celery on Windows '-P gevent' option is required
import os
from celery import Celery
from celery.schedules import crontab
import datetime
import pytz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal_project.settings')

app = Celery('news_portal_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# nofun function override to specify timezone
def nowfun():
    return datetime.datetime.now(pytz.timezone('Europe/Moscow'))


app.conf.beat_schedule = {
    'newsletter_every_monday_8am': {
        'task': 'news_portal_app.tasks.newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday', nowfun=nowfun)
    },
}
