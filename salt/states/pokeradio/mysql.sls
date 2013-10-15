#
# pokeradio.mysql
#
# Create database
#

# Required for salt to create databases
pokeradio_ensure_libmysqlclient_installed:
  pkg:
    - installed
    - name: libmysqlclient-dev

# Required for salt to create databases
pokeradio_ensure_python_mysqldb_installed:
  pkg:
    - installed
    - name: python-mysqldb
    - require:
      - pkg: mysql_install
      - pkg: mysql_client_install
      - pkg: pokeradio_ensure_libmysqlclient_installed

# Create the actual DB
pokeradio_create_mysql_databses:
  mysql_database:
    - present
    - name: {{ pillar['project_name'] }}
    - require:
      - pkg: pokeradio_ensure_python_mysqldb_installed