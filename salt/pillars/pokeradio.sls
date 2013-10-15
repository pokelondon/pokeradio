# Projeect Pillars (Variables)
# These are used by salt states to provision the instance to the pillars below.

# Project
user: vagrant
project_client: ''
project_name: 'pokeradio'

# Paths
root_dir: /home/vagrant
virtualenv_dir: /home/vagrant/.virtualenvs
home_dir: /home/vagrant

# Config
nginx_conf: /home/vagrant/pokeradio/src/pokeradio/config/dev/nginx.conf
post_activate: /home/vagrant/.virtualenvs/pokeradio/bin/postactivate