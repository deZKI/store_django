#!/bin/sh
python manage.py makemigrations
python manage.py migrate
RUN python manage.py collectstatic --noinput
gunicorn store_django.wsgi:application --bind 0.0.0.0:8000
celery --app store_django worker -l info  -l info