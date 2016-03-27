# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"

# Virtualbox VBoxManage customization docs - https://goo.gl/9J32dw
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    #vb.name = "cbr_system"
    vb.customize ["modifyvm", :id, "--name", "cbr_system", "--memory", "2048", "--cpus", "2", "--cpuexecutioncap", "50"]
  end

  config.vm.provision "shell", path: "bootstrap.sh"

end
