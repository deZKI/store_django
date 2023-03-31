#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/games.json
gunicorn store_django.wsgi:application --bind 0.0.0.0:8000