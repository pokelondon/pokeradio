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
