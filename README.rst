# Poke Pokeradio #
================

Description
-----------

Please enter a project description here.

Dependencies
------------

1. VirutalBox
2. Vagrant 1.1+
3. Poke Salt States Installed
4. Vagrant Guest Addtions Gem
5. Salt Vagrant Provisioner Gem

1. Install VirtualBox
+++++++++++++++++++++

Just grab the installer from the Virtualbox site:

https://www.virtualbox.org/wiki/Downloads

2. Install Vagrant
++++++++++++++++++

Grab the installer from the Vagrant site:

http://downloads.vagrantup.com

3. Install the Poke Salt States
+++++++++++++++++++++++++++++++

The Poke Salt States are the same states we use in production as well as development. One State Tree to rule them all as they say. If you have not already done so run:

``curl -L -u 'your_github_username' https://raw.github.com/pokelondon/Salt-States/master/tools/install.sh | sh``

Replace **your_github_username** with your GitHub user name. This will install the Poke Salt States to `~/.salt-poke`.

4. Guest Additions Plugin Installation
++++++++++++++++++++++++++++++++++++++

To ensure your Vagrant Box also ways has the guest additions most suitable to your VirtualBox version, from the OSX command line run:

``vagrant plugin install vagrant-vbguest``

When you run ``vagrant up`` the guest additions for your box will be installed automatically.

If you upgrade your VirtualBox to a new version you will need to run ``vagrant reload`` for the new guest additions version to be installed.

5. Salt Vagrant Provisioner
+++++++++++++++++++++++++++

To install the Salt Provisioner run the following command on OSX:

``vagrant plugin install vagrant-salt``

Installation
------------

This project is based on Varagnt. Please see the wiki documentation for getting your base Vagrant setup ready: http://dokuwiki.inside.poke/dokuwiki/doku.php?id=vagrant. The rest of this readme assumes you have this done.

 1. Clone the repository into ~/Development/poke/pokeradio/ or where ever you feel is appropriate for you.
 2. Run ``vagrant up`` from the project root.
 3. Once ``vagrant up`` has finished ssh into the instance: ``vagrant ssh``.
 4. The virtual environment should already be created and the projected installed to it, so just ``workon pokeradio``
 5. You will need to create a datamase so run the sync db command by running ``make syncdb``
 6. Run the django server by running ``make run_django``
 7. Run a instance of reddis 
 8. Run ``mopidy`` if you get an gdobject module error run ``export PYTHONPATH=/home/vagrant/.virtualenvs/pokeradioclient2/local/lib/python2.7/site-packages/:/usr/lib/python2.7/dist-packages``

Developers
----------

 * John Doe
