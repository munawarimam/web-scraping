### Quick Start

```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver

NB : Make sure you have changed your local CHROME_DRIVER path on webscraping/settings.py
```

### Dockerizing

```
$ docker build --tag web-scraping . 
$ docker run -d --publish 8000:8000 web-scraping
```