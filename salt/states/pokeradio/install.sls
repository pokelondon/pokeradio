#
# pokeradio.install
#
# Install pokeradio onto the virtual environment.
#

{{ pillar['project_name'] }}_install:
  cmd:
    - run
    - name: 'source /home/vagrant/.virtualenvs/{{ pillar['project_name'] }}/bin/activate && make develop'
    - cwd: /home/vagrant/{{ pillar['project_name'] }}
    - user: vagrant
    - group: vagrant
    - require:
      - virtualenv: {{ pillar['project_name'] }}_virtualenv
      - pip.installed: ensure_distibute_upgrade
      - mysql_database: {{ pillar['project_name'] }}_create_mysql_databses
      - file: /home/vagrant/.pypirc
      - file: /home/vagrant/.pip/pip.conf