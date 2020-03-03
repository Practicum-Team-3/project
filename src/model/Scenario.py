import json
from unique_id import get_unique_id
from datetime import datetime
from model.ExploitInfo import ExploitInfo
from model.FileManager import FileManager
from model.VulnerabilityInfo import VulnerabilityInfo

class Scenario(object):

    def __init__(self, scenario_name):
        self.file_manager = FileManager()
        #Variables
        self.scenario_name =  scenario_name
        self.scenario_id =  get_unique_id(length=8)
        now = datetime.now()
        self.creation_date = now.strftime("%d/%m/%Y %H:%M:%S")
        self.last_accessed = self.creation_date[:]
        self.exploit_info = ExploitInfo("" , "" , "")
        self.vulnerability_info = VulnerabilityInfo("" , "" , "" , "")
        self.machines = dict()

    def setExploitInfo(self , exploit_info):
        self.exploit_info = exploit_info
    
    def setVulnerabilityInfo(self , vulnerability_info):
        self.vulnerability_info = vulnerability_info
        
    def addVM(self, vm):
        self.machines[vm.name] = vm

    def dictionary(self):
        scenario_dict = dict()
        scenario_dict["scenario_name"] = self.scenario_name
        scenario_dict["scenario_id"] = self.scenario_id
        scenario_dict["creation_date"] = self.creation_date
        scenario_dict["last_accessed"] = self.last_accessed
        scenario_dict["exploit_info"] = self.exploit_info.dictionary() if self.exploit_info else dict()
        scenario_dict["vulnerability_info"] = self.vulnerability_info.dictionary() if self.vulnerability_info else dict()
        scenario_dict["machines"] = dict()
        for name in self.machines:
          scenario_dict["machines"][name] = self.machines[name].dictionary()
        return scenario_dict
    
    def generateScenario(self, scenario_name):
        json_dict = self.dictionary()
        json_name = self.scenario_name + ".json"
        with open(self.file_manager.getScenariosPath() / scenario_name / "JSON" / json_name, 'w') as outfile:
          json.dump(json_dict, outfile)
        json_string = json.dumps(json_dict , indent = 2)
        print(json_string)
        return json_string
  