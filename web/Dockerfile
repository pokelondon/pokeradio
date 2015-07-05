FROM python:2.7.8
MAINTAINER Poke London

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN adduser --disabled-password --gecos '' celery_user
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY setup.py /usr/src/app/
ONBUILD RUN python setup.py develop
