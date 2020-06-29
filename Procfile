release: python manage.py migrate --noinput
web: gunicorn tolstoy_calendar.wsgi
worker: celery -A tolstoy_calendar worker -B