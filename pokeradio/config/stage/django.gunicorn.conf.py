"""
.. module:: pokeradio.config.stage.django.gunicorn.py
   :synopsis: Gunicorn configuration.
"""

# Where to store the PID
pidfile = '/tmp/poke_pokeradio_django_stage.pid'

# Where to bind to
bind = 'unix:/tmp/poke_pokeradio_django_stage.sock'

# Debug mode
debug = False

# Process Name
proc_name = 'poke_pokeradio_django_stage'

# Preload
preload_app = True

# Timeout
timeout = 60

# Workers
workers = 2

# Logs
base_log_dir = '/poke/data/www/poke/pokeradio/pokeradio_stage/logs/'
logfile = '{0}django.gunicorn.log'.format(base_log_dir)
errorlog = '{0}django.gunicorn.error.log'.format(base_log_dir)
loglevel = 'info'