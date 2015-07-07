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
There are quite a few config vars. Rename the example `.env` file, modify it and source it to your shell.
```sh
$ mv example.env .env && vim .env
```
###3. Build images
```sh
$ docker-compose build
```

###6. Database
There's a migration dependency for the history app. It should be fine, just migrate it first.
```sh
$ python manage.py syncdb
$ python manage.py migrate history # sorry
$ python manage.py migrate
```

### Development
We have a Gruntfile to compile LESS and reload the browser. That's about it. If you want to use that then:
```sh
$ npm install
$ grunt
```
