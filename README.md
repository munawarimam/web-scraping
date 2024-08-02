### Quick Start

```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver

NB : Make sure you have changed your local CHROME_DRIVER path on webscraping/settings.py
```

### Dockerize

```
$ docker-compose up --build --force-recreate -d
```

### Setup docker on instance

```
$ sudo yum update
$ sudo amazon-linux-extras install docker
$ sudo service docker start
$ sudo usermod -a -G docker ec2-user
$ sudo chkconfig docker on
$ sudo yum install -y git
$ sudo reboot

# Docker Compose

$ sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```