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
        scenario_json = self.scenario_manager.getScenario(scenario_name)
        self.file_manager.createMachineFolders(scenario_json)
        for machine_name in scenario_json["machines"]:
            machine = scenario_json["machines"][machine_name]
            machine_path = self.file_manager.getScenariosPath() / scenario_name / "Machines" / machine_name
            self.vagrant_file.vagrantFilePerMachine(machine , machine_path)
        result = {"result": True}
        return result

    def getAvailableBoxes(self):
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