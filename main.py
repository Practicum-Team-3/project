import subprocess
from VirtualMachine import VirtualMachine as VM
from VagrantFile import VagrantFile
from Provision import Provision

if __name__=="__main__":
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