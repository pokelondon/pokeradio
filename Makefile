#
# Make File for Poke | Pokeradio
#
# Use this make file to install the project and run convenience methods. For example:
#
# 	make developer
# 	make syncdb
# 	make run_django
#

remove_egg:
	rm -rf ./src/pokeradio.egg-info

install_develop_dependencies:
	pip install "file://`pwd`#egg=pokeradio[develop]" --use-mirrors

install_test_dependencies:
	pip install "file://`pwd`#egg=pokeradio[test]" --use-mirrors

develop: install_develop_dependencies remove_egg

test: install_test_dependencies remove_egg

syncdb:
	django-admin.py syncdb
	django-admin.py migrate

run_django:
	django-admin.py runserver 0.0.0.0:9000

notebook:
	django-admin.py shell_plus --notebook

run_socket:
	node src/pokeradio/socketserver/main.js

run_mopidy:
	PYTHONPATH=/usr/lib/python2.7/dist-packages/:/home/vagrant/.virtualenvs/pokeradio/local/lib/python2.7/site-packages/ /home/vagrant/.virtualenvs/pokeradio/bin/mopidy --config /home/vagrant/pokeradio/src/mopidy-pokeradio/mopidy_pokeradio/config/dev/mopidy.conf
