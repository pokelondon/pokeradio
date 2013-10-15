#
# pokeradio.nginx
#
# Symlink the nginx conf into the conf.d directory
#

/etc/nginx/conf.d/{{ pillar['project_name'] }}.conf:
  file.symlink:
    - target: {{ pillar['nginx_conf'] }}
    - require:
      - pkg: nginx