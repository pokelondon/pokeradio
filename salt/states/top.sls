#
# Vagrant Environment
# Defined in the minion-config on the Vagrant project template.
#

vagrant:

  '*':

    #
    # Required States - Poke standard configuration / packages
    #

    - poke
    - libs
    - nginx
    - python2

    - node
    - redis
    - memcached

    {% if pillar['db'] == "mysql" %}
    - mysql
    {% elif pillar['db'] == "postgres" %}
    - postgres
    {% endif %}

    # Set pillar['db'] to postgres if you want
    {% if pillar['db'] == "mysql" %}
    - mysql
    {% elif pillar['db'] == "postgres" %}
    - postgres
    {% endif %}

    #
    # Stuff to setup this project
    # EG folders, DB, venv etc.
    #

    - vagrant-dev

    #
    # Developer states (mounted to ~/.salt-dev)
    # Eg Vimrc, ZSHrc, SSH keys etc.
    #

    - developer

    #
    # Any other states to be included for the project
    # that aren't part of a standard role.
    # These should probably just be used for testing stuff
    # out, otherwise they should be a new role.
    #

    - project

  #
  # Roles for including extra bundles of requirements.
  # Eg, some projects need Redis
  #

  'roles:celery':
    - match: grain
    - redis

  'roles:imaging':
    - match: grain
    - imagemagick

  'roles:memcached':
    - match: grain
    - memcached
