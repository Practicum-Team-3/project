import json
from pathlib import Path
from model.FileManager import FileManager

class VagrantFile(object):   
  def __init__(self):
    self.file_manager = FileManager()

  def vagrantFileCreator(self , scenario_name):
    json_name = "".join([scenario_name, ".json"])
    path_to_file = self.file_manager.getScenariosPath() / scenario_name /  "JSON" / json_name
    with open( path_to_file) as json_file:
      vf = json.load(json_file)

    for machine_name in vf["machines"]:
        machine = vf["machines"][machine_name]
        buffer = ""
        file = open("Vagrantfile_"+machine["name"], "w")
        #Opening
        buffer = f"Vagrant.configure(\"2\") do |config|\n"
        #Machines
        buffer += f'\tconfig.vm.define "{machine["name"]}" do |{machine["name"]}|\n'
        buffer += f'\t\t{machine["name"]}.vm.box = "{machine["os"]}"\n'

        #setup static ip
        if not machine["network_settings"]["ip_address"]:
            buffer += f'\t\t{machine["name"]}.vm.network \"private_network\", ip: \"{machine["ipAddress"]}\"\n'

        #setup synced folders
        if machine["shared_folders"] != None:
          host = machine["shared_folders"][0]
          guest = machine["shared_folders"][1]
          buffer += f'\t\t{machine["name"]}.vm.synced_folder \"{host}\", \"{guest}\"\n'

        #set provision
        if "provisions" in machine:
            provisions = machine["provisions"]
            buffer += f'\t\t{machine["name"]}.vm.provision \"{provisions["provision_type"]}\", inline: <<-SHELL\n'
            for command in provisions["commands"]:
                buffer += f'\t\t\t{command}\n'
            buffer += f'\t\tSHELL\n'
        buffer += f'\tend\n'
        #GUI
        buffer += f"\tconfig.vm.provider \"virtualbox\" do |vb|\n"
        buffer += f"\t\tvb.gui = "
        if machine["gui"]:
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