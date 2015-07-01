FROM python:2.7.8
MAINTAINER Poke London
EXPOSE 8000

# Make a dir to mount the project to
RUN mkdir -p /usr/src/app/pokeradio

# Install requirements
COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

# Copy scripts to folder above pokeradio
COPY manage.py /usr/src/app/manage.py
COPY setup.py /usr/src/app/setup.py

WORKDIR /usr/src/app

# Mount project code
COPY ./pokeradio /usr/src/app/pokeradio

RUN python setup.py develop

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
