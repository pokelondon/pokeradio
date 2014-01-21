#!/usr/bin/env python

from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from sys import path

path.append(abspath(join(dirname(__file__), 'src')))

from pokeradio import __VERSION__


def read(fname):
    return open(join(dirname(__file__), fname)).read()

# Installation Dependencies
install_dependencies = [
    'Django >= 1.6, < 1.7',
    'MySQL-python == 1.2.4',
    'South == 0.7.6',
    'bootstrap-admin == 0.1.9',
    'django-picklefield == 0.3.0',
    'raven == 3.3.5',
    'gunicorn == 18.0',
    'django-extensions == 1.2.2',
    'socketIO-client == 0.4',
    'python-social-auth == 0.1.14',
    'TornadIO2 == 0.0.4',
    'redis == 2.8.0',
    'simplejson == 3.3.1',
    'django-debug-toolbar == 0.9.4',
    'tornado == 3.1',
    'simplejson == 3.3.1',
    'tornado-redis == 2.4.15',
    'musicbrainzngs == 0.4',
    'Pillow == 2.3.0',
    'requests==2.0.0',
]

# Test Dependencies
test_dependencies = [
    'coverage == 3.6',
    'django-nose == 1.1',
    'nose-cover3 == 0.1.0',
    'nose == 1.2.1',
    'specloud == 0.4.5',
]

# Development Dependencies
development_dependencies = test_dependencies + [
    'django-debug-toolbar',
    'pdbpp == 0.7.2',
    'tornado == 3.1',
    'pyzmq == 13.1.0',
    'ipython == 0.13.1',
    'velcro == 1.0.1',
]

setup(
    name='pokeradio',
    version=__VERSION__,
    author='Poke London ltd',
    author_email='developer@pokelondon.com',
    description='',
    long_description=read('README.rst'),
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_dependencies,
    include_package_data=True,
    dependency_links=[
        'https://github.com/evilkost/brukva/tarball/master/#egg=brukva-0.0.1',
    ],
    extras_require={
        'develop': development_dependencies,
        'test': test_dependencies,
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
