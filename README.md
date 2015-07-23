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
- docker-machine (if you want, for deployment)

###1. Clone the repo
```
$ git clone http://github.com/pokelondon/pokeradio
$ cd pokeradio
```

###2. Set Config
All installation specific configs are accessed from the environment variables. Modify the example with yours and name it `.env` for docker-compose to find.
```
$ mv example.env .env && vim .env
```

###3. Build images
The App is made up out of a few docker containers to run each service, webserver, redis, socket server etc. Docker Compose can be used to create them all and link them together.
Make sure boot2docker is running then do this:
```
$ docker-compose build
$ docker-compose up
```

###6. Database
There's a migration dependency for the history app. It should be fine, just migrate it first.
Run the migrations on the web container and create a super user as instructed.
```
$ docker-compose run --rm web python manage.py syncdb
$ docker-compose run --rm web python manage.py migrate history # sorry
$ docker-compose run --rm web python manage.py migrate
```

### Frontend
We have a Gruntfile to compile LESS and reload the browser. That's about it. If you want to use that then:
```
$ npm install
$ grunt
```
