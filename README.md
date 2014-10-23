#pokeradio
This is the main (complicated) part of the legendary PokeRadio; the social wedge between the (otherwise) good people of POKE.

##Also in this family:
- [**PokeRadio app**](https://github.com/pokelondon/pokeradio) ☜ This!
- [PokeRadio Socket Server](https://github.com/pokelondon/pokeradio-socketserver)
- [PokeRadio Mopidy Client](https://github.com/pokelondon/pokeradio-mopidy)

![Home Page](doc/homepage.png?raw=true)

[Moar screenshotz](doc/screenshots.md)

## Running Locally

###You need:
- Virtualenv
- pip
- Postgres.app
- A Google OAuth API account and credentials
- Ngrok - For tunnelling OAuth callbacks
- libjpeg


###1. Clone the repo
```sh
$ git clone http://github.com/pokelondon/pokeradio
$ cd pokeradio
```
###2. Make Virtualenv
```sh
$ mkvirtualenv prad
```

###3. Make sure there's a dev DB running locally
(Postgres.app is good for this)
```sh
$ psql
```
and
```SQL
CREATE DATABASE pokeradio;
```
###4. Install Requirements, and the Django project.
```
$ pip install -r requirements.txt
$ python setup.py develop
```

If psycopg wont play ball, you might need to tell it where `pg_config` is:
```sh
$ export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.3/bin
```

###5. Set Config
There are quite a few config vars. Rename the example `.env` file, modify it and source it to your shell.
```sh
$ mv example.env .env && vim .env
$ source .env
```

###6. Database
There's a migration dependency for the history app. It should be fine, just migrate it first.
```sh
$ python manage.py syncdb
$ python manage.py migrate history # sorry
$ python manage.py migrate
```

###7. Oauth
Users login using OAuth with their Google account.
For this to work in dev, you need to [create an API token here](https://console.developers.google.com/project/190611052995/apiui/credential?authuser=0) go to "Create new Client ID"

You will need to provide a publicly accessible callback URL when the authroisation is complete. This will be the URL of the Heroku app for production, and a local tunnel for development. We use [Ngrok](https://ngrok.com/) for that. So add both urls here

Set the **Authorized Redirect URL** to
http://{yourhostname}/complete/google-oauth2/ where *yourhostname* is your Ngrock tunnel and your chosen Heroku app hostname.




#Deployment

Although we host ours on Amazon, to make it simple, below are the recommended instructions to get this puppy running on Heroku.

###You need:
- [**Heroku Toolbelt **](https://toolbelt.heroku.com/) + an account
- [**pokeradio--socketserver**](https://github.com/pokelondon/pokeradio-socketserver) running on another Heroku app (set this up after)

###1. Create and app, and setup addons
Call this something like _pokeradio_ (except you can't, we already did that)
```sh
$ heroku create
$ heroku addons:add heroku-postgresql:hobby-dev
$ heroku addons:add rediscloud
$ git push heroku master
```
###1.1 Socket Server
To notify users of changes to the playlist while they have the page open, we send realtime events over a websocket. To do this, a Node.JS socket server listens to events from this app via a Redis PubSub proxy. If you want to use this, follow the instructions for [**pokeradio--socketserver**](https://github.com/pokelondon/pokeradio-socketserver)

It has to connect to the same redisserver that you create for this app. You can get that from running
```sh
$ heroku config --shell | grep REDISCLOUD_URL
```


###2. Set Config
There are a lot of config vars that need to be exported to the Heroku environment
Included in the project is a template `.env` file for local development

If you chose to run the socket server, add the URL of the Heroku app to the config
```sh
$ heroku config:set SOCKETSERVER_HOST={yoursocketserver.herokuapp.com}
```
Repeat this process for the other vars that you've configured in `.env`

When the config is ready, setup the database and start the app.
```
$ heroku run python manage.py syncdb
$ heroku run python manage.py migrate history
$ heroku run python manage.py migrate
$ heroku ps:scale web=1
```

###3. Async
We have a lot of democracy in our studio, so much that it makes it a bit slow when some joker puts on Chas & Dave.
Therefore in the intrests of scalability, we've moved some of the computational flim-flam into a Celery queue. If you want to run this, you'll need to scale up a worker for it
```sh
$ heroku ps:scale web=1
```
... and thus exhausting the free tier


### Development
We have a Gruntfile to compile LESS and reload the browser. That's about it. If you want to use that then:
```sh
$ mv _package.json package.json && npm install; mv package.json _package.json # Sorry!
$ grunt
```

## TODO
- document lights webhook
- s3 profile pics and albumart
- make slack and pusher optional if the config is absent
