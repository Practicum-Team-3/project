import os
import subprocess

class VM(object):
    def __init__(self, Name, OS):
        self.os = OS
        self.name = Name
        self.shared_folders = [] #tuples of (hostPath, guestPath)
        self.ipAddress = None
        self.provision = None #will be populated by provision objects

    def setOS(self, os):
        self.os = os

    def setName(self, name):
        self.name = name

    def addSharedFolder(self, hostPath, guestPath):
        self.shared_folders.append((hostPath, guestPath))

    def setIPAddress(self, address):
        self.ipAddress = address

    def setProvision(self, provision):
        self.provision = provision


class Provision(object):
    def __init__(self, name):
        self.name = name
        self.command = None
        self.type = None
    
    def setShellCommand(self, commandString):
        self.type = "shell"
        self.command = commandString


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

#create the shared folders in host
# cwd = os.getcwd()
# try:
#     os.mkdir(f"{cwd}\\attackerfiles")
#     os.mkdir(f"{cwd}\\victimfiles")
# except OSError:
#     print("Creation of the directory %s failed" % f"{cwd}\sharedfolder")
# else:
#     print("Successfully created the directory %s " % f"{cwd}\sharedfolder")

#Create one attacker VM and one victim VM
attacker = VM("attacker", "laravel/homestead")
victim = VM("victim", "laravel/homestead")

#Link any shared folders from host to the VMs
attacker.addSharedFolder("./attackerfiles", "/sharedfolder")
victim.addSharedFolder("./victimfiles", "/sharedfolder")

#Set up network interfaces on VMs
attacker.setIPAddress("192.168.50.5")
victim.setIPAddress("192.168.50.6")

#Prepare Vagrantfile
vfile = VagrantFile()
vfile.addVM(attacker)
vfile.addVM(victim)
vfile.enableGUI(True)
vfile.write()

#Spin up the VMs
process = subprocess.Popen(['cmd', '/c','vagrant', 'up'], stdout=subprocess.PIPE, universal_newlines=True)
while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

#Add provisions to test network connectivity
pingAttacker = Provision("pingAttacker")
pingAttacker.setShellCommand("ping -c 4 192.168.50.5")
victim.setProvision(pingAttacker)

pingVictim = Provision("pingVictim")
pingVictim.setShellCommand("ping -c 4 192.168.50.6")
attacker.setProvision(pingVictim)

vfile.write()

#Run provisions
print("Testing Connectivity...")
process = subprocess.Popen(['cmd', '/k', 'vagrant', 'provision'], stdout=subprocess.PIPE, universal_newlines=True)
while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

#Add provisions to install software on VMs
runMalwareProvision = Provision("installE0")
runMalwareProvision.setShellCommand("./../../sharedfolder/e0.sh")
attacker.setProvision(runMalwareProvision)

runPOVProvision = Provision("installP0")
runPOVProvision.setShellCommand("./../../sharedfolder/p0.sh")
victim.setProvision(runPOVProvision)

vfile.write()

#Mock software installation
print("Installing software...")
process = subprocess.Popen(['cmd', '/k','vagrant', 'provision'], stdout=subprocess.PIPE, universal_newlines=True)
while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())




