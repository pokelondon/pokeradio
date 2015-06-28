FROM python:2.7.8
MAINTAINER Poke London
EXPOSE 8000

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/requirements.txt

WORKDIR /usr/src/python
RUN pip install -r /usr/src/requirements.txt

ENV DATABASE_URL postgres://postgres@db/postgres
ENV REDIS_URL redis://redis:6379

WORKDIR /usr/src/app
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

FROM ubuntu:14.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update
RUN apt-get install -y python python-pip python-dev libpq-dev git redis-server memcached
ADD . /home/docker/app


RUN pip install -r /home/docker/app/requirements.txt
RUN (cd /home/docker/app/ && python manage.py syncdb --noinput)
RUN (cd /home/docker/app/ && python manage.py collectstatic --noinput)
RUN touch /home/docker/app/pokeradio.sqlite
WORKDIR /home/docker/app/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
