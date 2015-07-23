FROM google/nodejs
MAINTAINER Poke London
EXPOSE 8080

COPY src /usr/src/app
WORKDIR /usr/src/app
RUN npm install

CMD /nodejs/bin/node main.js

