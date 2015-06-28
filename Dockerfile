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
