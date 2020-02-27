import json
from pathlib import Path

class VagrantFile(object):   
  def __init__(self):
    self.current_path = Path.cwd()
    self.scenarios_path = self.current_path / "scenarios"

    print(self.current_path)
    print(self.scenarios_path)
    
  def vagrantFileFromJSON(self , jsonFile):
    buffer = ""
    with open(self.scenarios_path / jsonFile) as json_file:
      vf = json.load(json_file )
    
    file = open("Vagrantfile", "w")
    #Opening
    buffer = f"Vagrant.configure(\"2\") do |config|\n"
    #Machines
    for machine in vf["machines"]:
        buffer += f'\tconfig.vm.define "{machine["name"]}" do |{machine["name"]}|\n'
        buffer += f'\t\t{machine["name"]}.vm.box = "{machine["os"]}"\n'
  
        #setup static ip
        if machine["ipAddress"] != None:
            buffer += f'\t\t{machine["name"]}.vm.network \"private_network\", ip: \"{machine["ipAddress"]}\"\n'
        
        #setup synced folders
        if machine["shared_folders"] != None:
          host = machine["shared_folders"][0]
          guest = machine["shared_folders"][1]
          buffer += f'\t\t{machine["name"]}.vm.synced_folder \"{host}\", \"{guest}\"\n'
  
        #set provision
        if "provision" in machine:
            for command in machine["provision"]["commands"]:
              buffer += f'\t\t{machine["name"]}.vm.provision \"{command[0]}\", inline: \"{command[1]}\"\n'
  
        buffer += f'\tend\n'
    #GUI
    buffer += f"\tconfig.vm.provider \"virtualbox\" do |vb|\n"
    buffer += f"\t\tvb.gui = "
    if vf["gui"]:
        buffer += "true\n"
    else:
        buffer += "false\n"
    buffer += f'\t\tvb.memory = \"1024\"\n'
    buffer += f"\tend\n"
    buffer += f"\nend\n"
  
    print(buffer)
  
    file.write(buffer)
    file.close()
    return vf