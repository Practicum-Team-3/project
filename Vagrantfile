Vagrant.configure("2") do |config|
	config.vm.define "attacker" do |attacker|
		attacker.vm.box = "laravel/homestead"
		attacker.vm.network "private_network", ip: "192.168.50.5"
		attacker.vm.synced_folder "./attackerfiles", "/sharedfolder"
	end
	config.vm.define "victim" do |victim|
		victim.vm.box = "laravel/homestead"
		victim.vm.network "private_network", ip: "192.168.50.6"
		victim.vm.synced_folder "./victimfiles", "/sharedfolder"
	end
	config.vm.provider "virtualbox" do |vb|
		vb.gui = "true"
		vb.memory = "1024"
	end

end
