import subprocess
import json
from pathlib import Path
from model.VirtualMachine import VirtualMachine as VM
from model.Scenario import Scenario
from model.ExploitInfo import ExploitInfo
from model.VulnerabilityInfo import VulnerabilityInfo
from model.NetworkSettings import NetworkSettings
from model.Provision import Provision
from model.ScenarioManager import ScenarioManager
from model.VagrantFile import VagrantFile

if __name__ == "__main__":
  scenarioManager = ScenarioManager()
  vagrantFile = VagrantFile()
  attacker = VM("attacker", "laravel/homestead" , True)
  victim = VM("victim", "laravel/homestead")
  
  #Link any shared folders from host to the VMs
  attacker.addSharedFolder("./attackerfiles", "/sharedfolder")
  victim.addSharedFolder("./victimfiles", "/sharedfolder")
    
  #Exploit info
  e_info = ExploitInfo("test_name" , "test_type" , "test_download_link")
  
  #Vulnerability info
  v_info = VulnerabilityInfo("test_name" , "test_type" , "test_cve_link" , "test_download_link")
  
  #Network settings
  n_settings = NetworkSettings("Network Name" , "Network Type" , "192.168.50.5" , True)
  n_settings_2 = NetworkSettings("Network Name" , "Network Type" , "192.168.50.6" , True)
  attacker.setNetworkSettings(n_settings)
  victim.setNetworkSettings(n_settings_2)
  
  #Provision
  provision = Provision("pingVictim")
  provision.setShellCommand("pip install unique-id")
  attacker.setProvision(provision)
  victim.setProvision(provision)
  
  #Prepare Scenario
  scenario_name = "Scenario_1"
  #Create empty scenario
  scenarioManager.createScenario(scenario_name)
  #Create custom scenario
  scenario = Scenario(scenario_name)
  scenario.setExploitInfo(e_info)
  scenario.setVulnerabilityInfo(v_info)
  scenario.addVM(attacker)
  scenario.addVM(victim)
  json_name = "".join([scenario_name, ".json"])
  with open(Path.cwd() / "scenarios" / scenario_name / "JSON" / json_name, 'w') as outfile:
    json.dump(scenario.dictionary(), outfile)
  json_string = json.dumps(scenario.dictionary(), indent=2)
  print(json_string)
  vagrantFile.vagrantFileCreator(scenario_name)
  
  '''
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
'''



