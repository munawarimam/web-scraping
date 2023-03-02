python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn webscraping.wsgi:application --workers=4 --bind 0.0.0.0:8000 --timeout 2700