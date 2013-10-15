#
# pokeradio.virtualenv
#
# Create project virtual environment.
#

{{ pillar['project_name'] }}_virtualenv:
  virtualenv:
    - managed
    - name: /home/vagrant/.virtualenvs/{{ pillar['project_name'] }}
    - no_site_packages: True
    - runas: vagrant
    - require:
      - file.directory: /home/vagrant/.virtualenvs
      - pkg: python-virtualenv

{{ pillar['project_name'] }}_post_activate_exists:
  file.touch:
    - name: /home/vagrant/.virtualenvs/{{ pillar['project_name'] }}/bin/postactivate
    - user: vagrant
    - group: vagrant
    - mode: 755
    - require:
      - virtualenv: {{ pillar['project_name'] }}_virtualenv

{{ pillar['project_name'] }}_post_activate_content:
  file.append:
    - name: /home/vagrant/.virtualenvs/{{ pillar['project_name'] }}/bin/postactivate
    - text:
      - 'cd /home/vagrant/{{ pillar['project_name'] }}'
      - 'export DJANGO_SETTINGS_MODULE={{ pillar['project_name'] }}.config.dev.settings'
    - require:
      - file: {{ pillar['project_name'] }}_post_activate_exists

ensure_distibute_upgrade:
  pip:
    - installed
    - name: distribute
    - user: vagrant
    - cwd: /home/vagrant
    - upgrade: True
    - bin_env: /home/vagrant/.virtualenvs/{{ pillar['project_name'] }}/bin/pip
    - require:
      - virtualenv: {{ pillar['project_name'] }}_virtualenv