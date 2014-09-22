# Projeect Pillars (Variables)
# These are used by salt states to provision the instance to the pillars below.

# Project
user: vagrant
project_client: 'poke'
project_name: 'pokeradio'

# Paths
root_dir: /home/vagrant
virtualenv_dir: /home/vagrant/.virtualenvs
home_dir: /home/vagrant

# Set which type of DB you would like (mysql|postgres)
db: mysql
