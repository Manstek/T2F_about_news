import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'T2F_about_news.settings')
app = Celery('T2F_about_news')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
