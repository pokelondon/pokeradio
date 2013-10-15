#
# pokeradio Module
#

include:
  - pokeradio.nginx  # Nginx config symlinks
  - pokeradio.mysql  # Mysql DB creation
  - pokeradio.virtualenv  # Python virtual environment creation
  - pokeradio.gitflow  # This project uses Git Flow
  - pokeradio.pypirc  # Use the poke pypi
  - pokeradio.pip  # Set pip to use the poke pypi
  - pokeradio.install  # Install pokeradio