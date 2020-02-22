class VagrantFile(object):
    def __init__(self, version=2):
        self.buffer = f"Vagrant.configure(\"{str(version)}\") do |config|\n"
        self.machines = {}
        self.gui = False

    def addVM(self, VM):
        self.machines[VM.name] = VM

    def enableGUI(self, isVisible):
        self.gui = isVisible

    def _initFile(self,version=2):
        self.buffer = f"Vagrant.configure(\"{str(version)}\") do |config|\n"

    def write(self):
        '''
        try:
            os.remove("Vagrantfile")
        except OSError as e: # name the Exception `e`
            print( f'Failed with:{e.strerror}')# look what it says
            print(f'Error code: {e.code}')
        '''
        open("Vagrantfile", 'w').close()

        self._initFile()
        file = open("Vagrantfile", "w")
        for name, machine in self.machines.items():
            self.buffer += f'\tconfig.vm.define "{machine.name}" do |{machine.name}|\n'
            self.buffer += f'\t\t{machine.name}.vm.box = "{machine.os}"\n'

            #setup static ip
            if machine.ipAddress != None:
                self.buffer += f'\t\t{machine.name}.vm.network \"private_network\", ip: \"{machine.ipAddress}\"\n'
            
            #setup synced folders
            if len(machine.shared_folders) > 0:
                for pair in machine.shared_folders:
                    self.buffer += f'\t\t{machine.name}.vm.synced_folder \"{pair[0]}\", \"{pair[1]}\"\n'

            #set provision
            if machine.provision != None:
                self.buffer += f'\t\t{machine.name}.vm.provision \"{machine.provision.type}\", inline: \"{machine.provision.command}\"\n'

            self.buffer += f'\tend\n'
        
        self.buffer += f"\tconfig.vm.provider \"virtualbox\" do |vb|\n"
        self.buffer += f"\t\tvb.gui = "
        if self.gui:
            self.buffer += "\"true\"\n"
        else:
            self.buffer += "\"false\"\n"
        self.buffer += f"\t\tvb.memory = \"1024\"\n"
        self.buffer += f"\tend\n"

        print(self.buffer)

        file.write(self.buffer)
        file.write("\nend\n")
        file.close()