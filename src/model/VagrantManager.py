import os
import subprocess
import re
from model.FileManager import FileManager
from model.VagrantFile import VagrantFile
from model.ScenarioManager import ScenarioManager

class VagrantManager(object):

    def __init__(self):
        self.file_manager = FileManager()
        self.vagrant_file = VagrantFile()
        self.scenario_manager = ScenarioManager()

    def createVagrantFiles(self, scenario_name):
        """
        Creates a vagrant file per machine in a scenario
        :param scenario_name: String with the scenario name
        :return: True if vagrant files were successfully created
        """
        scenario_json = self.scenario_manager.getScenario(scenario_name)
        self.file_manager.createMachineFolders(scenario_json)
        for machine_name in scenario_json["machines"]:
            machine = scenario_json["machines"][machine_name]
            machine_path = self.file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
            print(self.vagrant_file.vagrantFilePerMachine(machine , machine_path))
        result = {"result": True}
        return result

    def runVagrantUp(self, scenario_name):
        """
        Executes the vagrant up command for each machine in the scenario
        :param scenario_name: String with the scenario name
        :return: True if the vagrant up commands were successfully executed
        """
        self.createVagrantFiles(scenario_name)
        scenario_json = self.scenario_manager.getScenario(scenario_name)
        for machine_name in scenario_json["machines"]:
            machine_path = self.file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
            if not os.path.exists(machine_path):  # Proceed if path exists
                return
            os.chdir(machine_path)
            process = subprocess.Popen(['vagrant', 'up'], stdout=subprocess.PIPE,
                                       universal_newlines=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
        result = {"result": True}
        return result

    def getAvailableBoxes(self):
        """
        Gets the available boxes in the Vagrant context
        :return: A list of string with the available boxes
        """
        # Variables
        boxes = {}
        boxNum = 0
        boxlist = subprocess.check_output("vagrant box list", shell=True)
        boxlist = str(boxlist)
        boxlist = re.sub(r"(^[b']|'|\s(.*?)\\n)", " ", boxlist)
        boxlist = boxlist.split(" ")
        boxlist = filter(None, boxlist)

        print("Loading available Vanilla VMs")

        for boxName in boxlist:
            boxNum = boxNum + 1
            boxes[boxNum] = boxName
            print("[ " + str(boxNum) + " ]" + boxName)
        return boxes