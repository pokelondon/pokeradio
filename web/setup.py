#!/usr/bin/env python

from os.path import abspath, dirname, join
from setuptools import setup, find_packages
from sys import path

path.append(abspath(join(dirname(__file__), 'pokeradio')))


def read(fname):
    return open(join(dirname(__file__), fname)).read()

setup(
    name='pokeradio',
    author='Poke London ltd',
    author_email='developer@pokelondon.com',
    description='',
    zip_safe=False,
    package_dir={'': 'pokeradio'},
    packages=find_packages('pokeradio'),
    include_package_data=True,
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
