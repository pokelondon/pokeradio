import os
from fabric.api import env
from fabric.state import output

from velcro.env import bootstrap as _bootstrap
from velcro.decorators import pre_hooks, post_hooks
from velcro.http.nginx import (restart_nginx, reload_nginx, stop_nginx,
                              start_nginx)
from velcro.service.supervisord import list_programs, start, stop, restart
from velcro.scm.git import deploy as _deploy
from velcro.target import live, stage
from velcro.py.django import syncdb, migrate

# Silence Output
output['running'] = False

# Project Details
env.client = 'poke'
env.project = 'pokeradio'

env.local_path = os.path.abspath(os.path.dirname(__file__))

# Paths & Directories
env.root_path = '/poke/data/www/'
env.directories = {
    'media': None, 'static': None, 'logs': None, 'src': None,
}

# Users
env.user = 'poke'
env.sudo_user = 'root'

# Version Control
env.scm = 'git'

# Hosts to deploy too
env.hosts = [
    'oddish.pokedev.net'
]

# Config path
env.config_path_pipeline = [
    'src',
    '{package_name}',
    '{config_dir}',
    '{target}',
]

# HTTP Server
env.http_server_conf_path = '/poke/data/conf/nginx/'
env.nginx_conf = 'nginx.conf'

# Python Settings
env.py_venv_base = '/poke/data/python-virtualenvs'

# Django Settings
env.django_settings_module = '{project}.config.{target}.settings'

# Supervisord Configs
env.supervisord_config_dir = '/poke/data/conf/supervisord/'
env.supervisord_configs = [
    'supervisord.conf',
]


@pre_hooks(
    'velcro.db.mysql.create_database')
@post_hooks(
    'velcro.py.venv.create',
    'velcro.py.django.export_settings_module',
    'velcro.http.nginx.symlink',
    'velcro.service.supervisord.symlink',
)
def bootstrap():
    _bootstrap()


@post_hooks(
    'velcro.py.venv.setup',
    'velcro.scm.git.clean',
    'velcro.py.django.collectstatic',
    'velcro.service.supervisord.symlink',
    'service.supervisord.reread',
)
def deploy(branch, **kwargs):
    _deploy(branch)