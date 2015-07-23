FROM python:2.7.8
MAINTAINER Poke London

RUN adduser --disabled-password --gecos '' celery_user

COPY setup.py /usr/src/app/setup.py
COPY pokeradio/__init__.py /usr/src/app/pokeradio/__init__.py

COPY requirements.txt /usr/src/app/requirements.txt
RUN cd /usr/src/app && pip install -r requirements.txt

COPY . /usr/src/app
RUN cd /usr/src/app && python setup.py develop

CMD django-admin.py runserver 0.0.0.0:8000
