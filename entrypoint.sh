python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn webscraping.wsgi:application --workers=5 --bind 0.0.0.0:8000 --timeout 2400