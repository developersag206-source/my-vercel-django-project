web: python manage.py migrate && python manage.py collectstatic --no-input && gunicorn todomanager.wsgi:application --bind 0.0.0.0:$PORT
