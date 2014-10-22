web: gunicorn pokeradio.wsgi:application --settings=pokeradio.config.settings --debug --log-file -
worker: celery -A pokeradio  worker --loglevel=error
