#
# pokeradio.pip
#
# Ensure pip uses poke pypi is the default index url
#

/home/vagrant/.pip:
  file:
    - directory
    - user: vagrant
    - group: vagrant
    - mode: 766
    - makeDirs: True

/home/vagrant/.pip/pip.conf:
  file:
    - managed
    - user: vagrant
    - group: vagrant
    - mode: 644
    - source: salt://pokeradio/files/pip.conf
    - require:
      - file.directory: /home/vagrant/.pip