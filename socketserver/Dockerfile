FROM google/nodejs
MAINTAINER Poke London
EXPOSE 8080

WORKDIR /usr/src/app
RUN git clone https://github.com/pokelondon/pokeradio-socketserver .
RUN npm install

ENV REDISCLOUD_URL redis://redis:6379/0

CMD ['/nodejs/bin/npm', 'start']
