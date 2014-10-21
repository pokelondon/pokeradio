"""
.. module:: pokeradio.config.live.sockets.gunicorn.py
   :synopsis: Gunicorn configuration.
"""

# Use the custom socketio worker class
worker_class = 'tornado'


# Where to store the PID
pidfile = '/tmp/poke_pokeradio_sockets_live.pid'

# Where to bind to
bind = 'unix:/tmp/poke_pokeradio_sockets_live.sock'

# Debug mode
debug = True

# Process Name
proc_name = 'poke_pokeradio_sockets_live'

# Preload
preload_app = True

# Timeout
timeout = 60

# Logs
base_log_dir = '/poke/data/www/poke/pokeradio/pokeradio_live/logs/'
logfile = '{0}sockets.gunicorn.log'.format(base_log_dir)
errorlog = '{0}sockets.gunicorn.error.log'.format(base_log_dir)
loglevel = 'info'
