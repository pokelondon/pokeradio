FROM ubuntu:14.04
RUN apt-get update
RUN apt-get install -y python python-pip python-dev libpq-dev git
RUN git clone https://github.com/pokelondon/pokeradio.git pokeradio
WORKDIR /pokeradio
RUN pip install -r requirements.txt
RUN python setup.py develop
EXPOSE 9000
CMD ["make", "run_django"]
