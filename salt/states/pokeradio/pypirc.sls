#
# pokeradio.pypi
#
# Ensure the default pypi index is set to poke pypi server.
#

/home/vagrant/.pypirc:
  file:
    - managed
    - user: vagrant
    - group: vagrant
    - mode: 644
    - source: salt://pokeradio/files/.pypirc