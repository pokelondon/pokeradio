#
# Top File
# States to run for this Virtual Machine.
#

# Vagrant Environment
vagrant:
  '*':
    # Required States - Poke standard configuration / packages
    - poke.bash
    - poke.packages
    # Extra Packages
    - nginx
    - ntp
    # Libs - Required for some Python modules
    - libjpeg
    - libxslt
    - libevent
    # States for this vm, based on project requirements, for example: python2
    - python2
    - mysql
    # Project Specific States in salt/states/ (same level as this top.sls)
    - pokeradio
    # Developer states (mounted to ~/.salt-dev)
    - developer