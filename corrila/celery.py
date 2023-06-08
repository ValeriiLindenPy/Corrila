import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corrila.settings')

app = Celery('corrila')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_transport_options = {
    'visibility_timeout': 3600,
    'ssl_cert_reqs': 'CERT_REQUIRED'
}

app.autodiscover_tasks()