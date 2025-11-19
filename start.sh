#!/bin/bash
# Startup script for Render - runs migrations and creates superuser on startup

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python create_superuser.py

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 manage_rent_home.wsgi:application
