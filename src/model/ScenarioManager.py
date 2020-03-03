import os
import json
from model.FileManager import FileManager
from model.Scenario import Scenario

class ScenarioManager(object):

    def __init__(self):
        self.file_manager = FileManager()

    def createScenario(self, scenario_name):
        #Folder creation moved to FileManager
        self.file_manager.createScenarioFolders(scenario_name)
        scenario = Scenario(scenario_name)
        scenario.generateScenario(scenario_name)
        result = {"result": True}
        return result

    def getScenarios(self):
        # Variables
        scenarios = os.listdir(self.file_manager.getScenariosPath())
        scenarios_dict = {"scenarios": scenarios}
        return scenarios_dict


    def scenarioExists(self, scenario_name):
        scenario_dir_path = self.file_manager.getScenariosPath() / scenario_name / "JSON"
        if not os.path.isdir(scenario_dir_path):
            print("Scenario %s directory not found" % scenario_name)
            return False
        else:
            scenario_json_path = scenario_dir_path /  ''.join([scenario_name, ".json"])
            if not os.path.exists(scenario_json_path):
                print("Scenario %s json not found" % scenario_name)
                return None
            else:
                return scenario_json_path

    def getScenario(self, scenario_name):
        scenario_json_path = self.scenarioExists(scenario_name)
        if scenario_json_path:
            try:
                with open(scenario_json_path) as json_file:
                    scenario_json = json.load(json_file)
                    return scenario_json
            except:
                print("Something went wrong while retrieving Scenario JSON")

    def editScenario(self, scenario_name , new_scenario):
        scenario_json_path = self.scenarioExists(scenario_name)
        if scenario_json_path:
            with open(scenario_json_path, 'w+') as outfile:
                outfile.write(json.dumps(new_scenario, indent=2))
                outfile.close()
            #THIS IS A PLACEHOLDER
            #It will try to create the folders every time the scenario is edited
            #new_scenario_dict = json.loads(new_scenario)
            return True
        else:
            return False

