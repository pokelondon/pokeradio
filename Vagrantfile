#!/usr/bin/ruby

#
# Vagrant File for Poke | Pokeradio
# Provisioner: Salt
# OS: Ubuntu 12.04 LTS 64Bit
#

Vagrant.configure("2") do |config|

    # Base Box - Hosted on S3
    config.vm.box = "ubuntu_precise64_blank"
    config.vm.box_url = "http://poke.vagrant.boxes.s3.amazonaws.com/ubuntu_precise64_blank.box"

    #
    # Port Forwarding / Assign static IP
    #

    # Nginx Port
    config.vm.network :forwarded_port, guest: 80, host: 8080
    # Ipython notebook
    config.vm.network :forwarded_port, guest: 8888, host: 8888
    config.vm.network :forwarded_port, guest: 8001, host: 8001
    config.vm.network :private_network, ip: "10.10.10.10"

    #
    # Virutalbox Settings - Remove this line if symlinks are not required
    #
    config.vm.provider :virtualbox do |v|
        v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
        v.gui = true
    end

    #
    # Synced Folders
    #

    # The Project Mount - This Directory
    config.vm.synced_folder ".", "/home/vagrant/pokeradio", :nfs => true

    # Project Salt Sates
    config.vm.synced_folder "./salt", "/srv/salt"

    # Poke Salt States
    local_poke_states = File.join(File.expand_path('~'), '.salt-poke')
    if File.directory?(local_poke_states)
        config.vm.synced_folder local_poke_states, "/home/vagrant/.salt-poke"
    else
        abort("Please install the Poke Salt States.")
    end

    # Local Developer States - Not in version control, this is for the developer to manage, e.g Git / Vim Configs
    # Developers should symlink this locally to ~/.salt-dev
    local_developer_states = File.join(File.expand_path('~'), '.salt-dev')
    if File.directory?(local_developer_states)
        config.vm.synced_folder local_developer_states, "/home/vagrant/.salt-dev"
    else
        $stdout.write "Vagrant: Warning: You do not have any local states\n"
    end

    #
    # Provisioner: Salt
    #

    config.vm.provision :salt do |s|
        s.run_highstate = true                           # Always run the Salt Proviosining System
        s.minion_config = "salt/config/minion.conf"      # Where the minion config lives
        s.install_type = "stable"
    end

end