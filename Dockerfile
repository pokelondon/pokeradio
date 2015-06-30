FROM python:2.7.8
MAINTAINER Poke London
EXPOSE 8000

# Make a dir to mount the project to
RUN mkdir -p /usr/src/app

# Install requirements
COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app

CMD [ "django-admin.py", "runserver", "0.0.0.0:8000" ]
