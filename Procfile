release: python manage.py migrate --noinput
web: gunicorn tolstoy_calendar.wsgi
worker: celery worker --app=tolstoy_calendar.celery.app -B