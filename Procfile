web: gunicorn corrila.wsgi --log-file -
worker: celery -A corrila worker --loglevel=info
flower: celery -A corrila flower