<center>
![PokeRadio](pokeradio/public/img/poke-radio-logo.png?raw=true)
</center>
###
This is the main (complicated) part of the legendary PokeRadio; the social wedge between the (otherwise) good people of POKE.

##Also in this family:
- [**PokeRadio app**](https://github.com/pokelondon/pokeradio) ☜ This!
- [PokeRadio Mopidy Client](https://github.com/pokelondon/pokeradio-mopidy)

<center>
![Home Page](doc/homepage.png?raw=true)
</center>

[**Moar screenshotz →**](doc/screenshots.md)

## Running Locally

###You need:
- Docker
- docker-compose

###1. Clone the repo
```sh
$ git clone http://github.com/pokelondon/pokeradio
$ cd pokeradio
```
###2. Set Config
There are quite a few config vars. Rename the example `.env` file with important variables for the app. Docker Compose will export it to the web container at runtime.
```sh
$ mv example.env .env && vim .env
```

###3. Build images
The App is made up out of a few docker containers to run each service, webserver, redis, socket server etc. Docker Compose can be used to create them all and link them together.
Make sure boot2docker is running then do this:
```sh
$ docker-compose build
$ docker-compose up
```

First time round, you need to create a database and user to match the credentials defined in your `.env` file. This can be done by attaching to the postgres container and running the following:
```sh
$ ssh boot2docker
$ docker exec -it pokeradio_postgres_1 bash
    $ psql
    $ CREATE USER pokeradio_user WITH PASSWORD 'prad$_Pa$$';
    $ ALTER USER pokeradio_user SUPERUSER;
    $ CREATE DATABASE mycms WITH OWNER = pokeradio_user;
    $ \q
    $ exit
```

###6. Database
There's a migration dependency for the history app. It should be fine, just migrate it first.
Run the migrations on the web container
```sh
$ ssh boot2docker
$ docker exec -it pokeradio_web_1 bash
    $ python manage.py syncdb
    $ python manage.py migrate history # sorry
    $ python manage.py migrate
```

### Frontend
We have a Gruntfile to compile LESS and reload the browser. That's about it. If you want to use that then:
```sh
$ npm install
$ grunt
```
